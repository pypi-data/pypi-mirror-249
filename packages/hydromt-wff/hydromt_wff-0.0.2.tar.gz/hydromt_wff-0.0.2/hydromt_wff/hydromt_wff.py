import numpy as np
import pandas as pd
import geopandas as gpd
import shapely.geometry
from shapely.geometry import box, mapping
import hydromt
from hydromt import DataCatalog, flw
from hydromt.workflows import get_basin_geometry
from hydromt.log import setuplog
from pyproj import CRS
from pyproj.aoi import AreaOfInterest
from pyproj.database import query_utm_crs_info
import shutil
import json
from geojson import Feature, FeatureCollection, dump
import os
from dem_stitcher.stitcher import stitch_dem, NoDEMCoverage
from osgeo import gdal, gdalconst
import pyflwdir
import rioxarray as rxr
import xarray as xr
import mercantile
import tempfile
import fiona
import folium
from folium.plugins import MousePosition, Draw
import matplotlib.pyplot as plt
import datetime as dt
import csv
import netCDF4
import math
import getpass
from scipy.stats import norm, gamma, weibull_min, genextreme, lognorm
import rasterio
from rasterio import mask, merge
from rasterio.features import geometry_mask
from rasterio.mask import mask
from rasterio.windows import Window
from rasterio.enums import Resampling
from rasterio.transform import from_origin
from rasterio.merge import merge
from rasterio.warp import calculate_default_transform, reproject, Resampling
import csv
from contextlib import ExitStack
from tqdm import tqdm
from tqdm import tqdm as tqdm_bar
import meshkernel
from meshkernel import (GeometryList, MeshKernel, MakeGridParameters)
import xugrid as xu
import glob
import tifffile as tiff
from hydrolib.core.dflowfm.mdu.models import FMModel, AutoStartOption
from hydrolib.core.dflowfm.net.models import *
from hydrolib.core.dflowfm.inifield.models import *
from hydrolib.core.dflowfm.bc.models import *
from hydrolib.core.dflowfm.ext.models import *

logger_dem = setuplog("Topographical_data", log_level=10) 
logger_basin = setuplog("Basin_delineation", log_level=10)
logger_roughness = setuplog("Roughness_map", log_level=10)
logger_infilt = setuplog("Infiltration_maps", log_level=10)
logger_meteo = setuplog("Hydrometeorological_data", log_level=10)

########################################################################################################################
#######################################      Basin Delineation      ####################################################
########################################################################################################################

def drainage_network(output_folder, bbox_input_method= '1'):
    """
    This function loads bounding box data and derives a drainage network based on specified input methods.

    Parameters
    ----------
    bbox_input_method : str
        Method for providing bounding box coordinates.
        Enter '1' to read the data from the drawn bounding box or '2' to use a user defined GeoJSON bounding box file.
    output_folder : str
        Path to the output folder for saving GeoJSON files.

    Returns
    -------
    Tuple of GeoDataFrames (gdf_bbox, gdf_riv) representing bounding box and drainage network.

    """
    #Bounding box coordinates
    if bbox_input_method == '1':
        file_name = "data.geojson"

        # Get the user's download folder path
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        # Construct the full path to the file
        data_path = os.path.join(download_folder, file_name)

        with open(data_path, 'r') as f:
            data = json.load(f)

        # Separate features based on geometry type
        polygon_features = [feature for feature in data['features'] if feature['geometry']['type'] == 'Polygon']
        point_features = [feature for feature in data['features'] if feature['geometry']['type'] == 'Point']

        # Create separate FeatureCollections for each geometry type
        polygon_collection = FeatureCollection(polygon_features)
        point_collection = FeatureCollection(point_features)

        # Save each FeatureCollection to a new GeoJSON file
        bbox_path= os.path.join(download_folder, 'geom.geojson')
        with open(bbox_path, 'w') as f:
            gdf_bbox= dump(polygon_collection, f)

        with open(os.path.join(download_folder, 'outletPoint.geojson'), 'w') as f:
            outlet= dump(point_collection, f)

        # Read the bounding box file
        gdf_bbox = gpd.read_file(bbox_path)

        #Get bounding box coordinates from the bounding box polygon
        lon_min, lat_min, lon_max, lat_max = gdf_bbox.geometry.total_bounds

    elif bbox_input_method == '2':
        # Provide the path to the bounding box file
        bbox_path = input("Enter the path to the bounding box file (e.g., '/path/to/bbox.geojson'): ")
        if not os.path.exists(bbox_path):
            print(f"The file {bbox_path} was not found.")
            exit()

        # Read the bounding box file
        gdf_bbox = gpd.read_file(bbox_path)

        # Get bounding box coordinates from the bounding box polygon
        lon_min, lat_min, lon_max, lat_max = gdf_bbox.geometry.total_bounds

    else:
        print("Invalid input method. Please enter '1' or '2'.")
        exit()

    data_catalog = hydromt.DataCatalog(logger=logger_basin, data_libs=["deltares_data"])
    bbox=[lon_min , lat_min , lon_max, lat_max ]
    # read MERIT hydro data
    ds = data_catalog.get_rasterdataset("merit_hydro", variables=["flwdir", "elevtn", "strord", "basins"], bbox=[lon_min - 1, lat_min - 1, lon_max + 1, lat_max + 1])
    basin_index = data_catalog.get_geodataframe("merit_hydro_index", bbox=bbox)

    # derive river geometry based on stream order >= 7
    flwdir = hydromt.flw.flwdir_from_da(ds["flwdir"], ftype="d8")
    feats = flwdir.streams(mask=ds["strord"] >= 7)
    gdf_riv = gpd.GeoDataFrame.from_features(feats)

    # bounds = [lon_min, lat_min, lon_max, lat_max]
    gdf_bounds = gpd.GeoDataFrame(geometry=[box(*bbox)], crs=4326)
    extent = gdf_bounds.buffer(0.05).total_bounds[[0, 2, 1, 3]]

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Export the GeoDataFrames to GeoJSON 
    gdf_bounds= gdf_bounds.to_crs(4326)
    gdf_bounds.to_file(os.path.join(output_folder, "bbox_4326.geojson"), driver="GeoJSON")
    gdf_riv.crs = CRS.from_epsg(4326)
    gdf_bounds.crs = CRS.from_epsg(4326) 

    # Define the target UTM zone based on the bounding box
    utm_crs_list = query_utm_crs_info(
        datum_name="WGS 84",
        area_of_interest=AreaOfInterest(
            west_lon_degree=lon_min,
            south_lat_degree=lat_min,
            east_lon_degree=lon_max,
            north_lat_degree=lat_max,
        ),
    )
    utm_crs = CRS.from_epsg(utm_crs_list[0].code)
    gdf_riv = gdf_riv.to_crs(utm_crs)
    gdf_bounds = gdf_bounds.to_crs(utm_crs)

    gdf_bounds_path = os.path.join(output_folder, "bbox.geojson")
    gdf_riv_path = os.path.join(output_folder, "drainage_network.geojson")

    gdf_bounds.to_file(gdf_bounds_path, driver="GeoJSON")
    gdf_riv.to_file(gdf_riv_path, driver="GeoJSON")

    print(f"Bounding box file saved to {gdf_bounds_path}")
    print(f"Drainage network file saved to {gdf_riv_path}")

    return gdf_bbox, gdf_riv

def drainage_map(gdf_bbox, gdf_riv):
    """
    Create a Folium map to visualize and interact with the bounding box and drainage network.

    Parameters
    ----------
    gdf_bbox : GeoDataFrame
        GeoDataFrame representing the bounding box (GeoJSON).
    gdf_riv : GeoDataFrame
        GeoDataFrame representing the drainage network (GeoJSON).

    Returns
    -------
    Folium map object.

    Notes
    -----
    This function allows users to draw a new bounding box on the map if the existing one does not cover the entire area of interest.
    Additionally, users can draw an outlet point based on the drainage network. After drawing these features, users can export the data,
    and it will be saved as a GeoJSON file containing the drawn features.

    """
    # Get bounding box coordinates from the bounding box polygon
    lon_min, lat_min, lon_max, lat_max = gdf_bbox.geometry.total_bounds
    AoI_bbox = folium.Map(location=[(lat_max + lat_min)/2, (lon_min + lon_max)/2], zoom_start=10)

    gdf_riv = gdf_riv.to_crs(4326)
    
    # Convert GeoDataFrames to GeoJSON for display on the map
    gdf_riv_geojson = gdf_riv.to_json()
    

    # Draw on Folium map
    Draw(export=True,
         filename='data.geojson',
         draw_options={"polyline": False, "polygon": False,
                       "circle": False, "circlemarker": False}
         ).add_to(AoI_bbox)

    #  Use folium.GeoJson to add the GeoJSON data to the map
    # Define the style in one command
    style_geom = {'color': 'red',
                  'weight2': 2,
                  'fill': True,
                  'fillColor': 'pink',
                  'fillOpacity': 0.5,}
    folium.GeoJson(gdf_bbox, name="Bounding Box", style_function=lambda x: style_geom).add_to(AoI_bbox)

    # Add river and basin layers to the map
    folium.GeoJson(gdf_riv_geojson, name="Drainage Network", style_function=lambda x: {
        'color': 'blue',
        'fillOpacity': 0.5
    }).add_to(AoI_bbox)

    MousePosition(position="topright", separator=" , ",
                  lat_formatter="function(num) {return L.Util.formatNum(num, 3) + ' &deg; ';};",
                  lng_formatter="function(num) {return L.Util.formatNum(num, 3) + ' &deg; ';};",
                  ).add_to(AoI_bbox)
    # Add a layer control
    folium.LayerControl(position='bottomright', collapsed=False).add_to(AoI_bbox)

    return AoI_bbox

def basin_delineation(output_folder, bbox_update_method= '2', outlet_input_method= '1'):
    """
    Generate the catchment delineation based on bounding box and outlet point data.

    Parameters
    ----------
    bbox_update_method : str
        Input method for bounding box.
        Enter '1' if a change was made for the firstly drawn bounding box or '2' if no change was made.
    outlet_input_method : str
        Input method for outlet point.
        Enter '1' to read data from the drawn outlet point or '2' to use a user defined GeoJSON outlet point file.
    output_folder : str
        Output folder to save GeoJSON files.

    Returns
    -------
    gdf_riv : GeoDataFrame
        GeoDataFrame representing the drainage network.
    gdf_bas : GeoDataFrame
        GeoDataFrame representing the basin.
    gdf_riv_clipped : GeoDataFrame
        GeoDataFrame representing the clipped drainage network.
    gdf_outlet : GeoDataFrame
        GeoDataFrame representing the outlet point.

    Notes
    -----
    This function prompts the user to input the method for defining the bounding box and outlet point.
    It reads GeoJSON files and calculates drainage network and basin based on the specified inputs.
    The results are saved in GeoJSON files in the specified output folder.

    """

    #Bounding box coordinates
    if bbox_update_method == '1':
        file_name = "data.geojson"

        # Get the user's download folder path
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        # Construct the full path to the file
        data_path = os.path.join(download_folder, file_name)

        with open(data_path, 'r') as f:
            data = json.load(f)

        # Separate features based on geometry type
        polygon_features = [feature for feature in data['features'] if feature['geometry']['type'] == 'Polygon']
        point_features = [feature for feature in data['features'] if feature['geometry']['type'] == 'Point']

        # Create separate FeatureCollections for each geometry type
        polygon_collection = FeatureCollection(polygon_features)
        point_collection = FeatureCollection(point_features)

        # Save each FeatureCollection to a new GeoJSON file
        with open(os.path.join(download_folder, 'geom.geojson'), 'w') as f:
            gdf_bbox= dump(polygon_collection, f)

        with open(os.path.join(download_folder, 'outletPoint.geojson'), 'w') as f:
            outlet= dump(point_collection, f)

        # Read the bounding box file
        gdf_bbox = gpd.read_file(os.path.join(download_folder, 'geom.geojson'))

        #Get bounding box coordinates from the bounding box polygon
        lon_min, lat_min, lon_max, lat_max = gdf_bbox.geometry.total_bounds
        geom_path = os.path.join(download_folder, 'geom.geojson')

    elif bbox_update_method == '2':
        # Provide the path to the bounding box file
        bbox_path = os.path.join(output_folder, 'bbox_4326.geojson')
        if not os.path.exists(bbox_path):
            print(f"The file {bbox_path} was not found.")
            exit()

        # Read the bounding box file
        gdf_bbox = gpd.read_file(bbox_path)

        # Get bounding box coordinates from the bounding box polygon
        lon_min, lat_min, lon_max, lat_max = gdf_bbox.geometry.total_bounds

    else:
        print("Invalid input method. Please enter '1' or '2'.")
        exit()
    
    # Outlet point coordinates
    if outlet_input_method == '1':
        if bbox_update_method == '2':
            # Read the outlet point file from the download folder
            download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            outlet_point_path = os.path.join(download_folder, "data.geojson")

        elif bbox_update_method == '1':
            # Read the outlet point file from the download folder
            download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
            outlet_point_path = os.path.join(download_folder, "outletPoint.geojson")

        # Check if the file exists
        if not os.path.exists(outlet_point_path):
            print(f"The file {outlet_point_path} was not found.")
            exit()

        # Read the outlet point file
        gdf_outlet = gpd.read_file(outlet_point_path)

        # Get longitude and latitude from the outlet point layer
        lon_outlet = gdf_outlet.geometry.x.iloc[0]
        lat_outlet = gdf_outlet.geometry.y.iloc[0]
                
    elif outlet_input_method == '2':
        # Provide the path to the outlet point file
        outlet_point_path = input("Enter the path to the outlet point file (e.g., '/path/to/outletPoint.geojson'): ")

        # Check if the file exists
        if not os.path.exists(outlet_point_path):
            print(f"The file {outlet_point_path} was not found.")
            exit()

        # Read the outlet point file
        gdf_outlet = gpd.read_file(outlet_point_path)

        # Get longitude and latitude from the outlet point layer
        lon_outlet = gdf_outlet.geometry.x.iloc[0]
        lat_outlet = gdf_outlet.geometry.y.iloc[0]
            
    else:
        print("Invalid input method. Please enter '1' or '2'.")
        exit()

    # instantiate instance of Data Catalog
    data_catalog = hydromt.DataCatalog(logger=logger_basin, data_libs=["deltares_data"])

    # read MERIT hydro data
    ds = data_catalog.get_rasterdataset("merit_hydro", variables=["flwdir", "elevtn", "strord", "basins"], bbox=[lon_min - 2, lat_min - 2, lon_max + 2, lat_max + 2])
    bbox=[lon_min , lat_min , lon_max, lat_max ]
    basin_index = data_catalog.get_geodataframe("merit_hydro_index", bbox=bbox)
    
    # derive river geometry based on stream order >= 7
    flwdir = hydromt.flw.flwdir_from_da(ds["flwdir"], ftype="d8")
    feats = flwdir.streams(mask=ds["strord"] >= 7)
    gdf_riv = gpd.GeoDataFrame.from_features(feats)

    # Get the basin based on a point location [x, y].
    xy = [lon_outlet, lat_outlet]
    gdf_bas, gdf_out = get_basin_geometry(
        ds= ds,
        kind="subbasin",
        xy=xy,
        strord=7,
        bounds=bbox,
        basin_index= basin_index,
        logger=logger_basin,
    )

    gdf_bounds = gpd.GeoDataFrame(geometry=[box(*bbox)], crs=4326)
    extent = gdf_bounds.buffer(0.05).total_bounds[[0, 2, 1, 3]]

    # Clip the river layer based on the basin boundaries
    gdf_riv_clipped = gpd.overlay(gdf_riv, gdf_bas, how="intersection")

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Export the GeoDataFrames to GeoJSON with the new paths
    gdf_bas= gdf_bas.to_crs(4326)
    gdf_bounds= gdf_bounds.to_crs(4326)
    gdf_bas.to_file(os.path.join(output_folder, "basin_4326.geojson"), driver="GeoJSON")
    gdf_bounds.to_file(os.path.join(output_folder, "bbox_4326.geojson"), driver="GeoJSON")

    gdf_riv.crs = CRS.from_epsg(4326)
    gdf_bas.crs = CRS.from_epsg(4326)
    gdf_riv_clipped.crs = CRS.from_epsg(4326)
    gdf_bounds.crs = CRS.from_epsg(4326) 

    # Define the target UTM zone based on the bounding box
    utm_crs_list = query_utm_crs_info(
        datum_name="WGS 84",
        area_of_interest=AreaOfInterest(
            west_lon_degree=lon_min,
            south_lat_degree=lat_min,
            east_lon_degree=lon_max,
            north_lat_degree=lat_max,
        ),
    )
    utm_crs = CRS.from_epsg(utm_crs_list[0].code)
    gdf_riv = gdf_riv.to_crs(utm_crs)
    gdf_bas = gdf_bas.to_crs(utm_crs)
    gdf_riv_clipped = gdf_riv_clipped.to_crs(utm_crs)
    gdf_bounds = gdf_bounds.to_crs(utm_crs)

    if bbox_update_method == '1':  
        gdf_bounds.to_file(os.path.join(output_folder, "bbox.geojson"), driver="GeoJSON")

    gdf_bas_path = os.path.join(output_folder, "basin.geojson")
    gdf_riv_clipped_path = os.path.join(output_folder, "stream.geojson")

    gdf_bas.to_file(os.path.join(output_folder, "basin.geojson"), driver="GeoJSON")
    gdf_riv_clipped.to_file(os.path.join(output_folder, "stream.geojson"), driver="GeoJSON")

    print(f"Basin file saved to {gdf_bas_path}")
    print(f"Stream file saved to {gdf_riv_clipped_path}")

    return gdf_bas, gdf_riv_clipped, gdf_outlet

def basin_map(gdf_bbox, gdf_riv, gdf_bas, gdf_riv_clipped, gdf_outlet):
    """
    Create a Folium map displaying the bounding box, drainage network, basin, stream, and outlet point.

    Parameters
    ----------
    gdf_bbox : GeoDataFrame
        GeoDataFrame representing the bounding box (GeoJSON).
    gdf_riv : GeoDataFrame
        GeoDataFrame representing the drainage network (GeoJSON).
    gdf_bas : GeoDataFrame
        GeoDataFrame representing the basin (GeoJSON).
    gdf_riv_clipped : GeoDataFrame
        GeoDataFrame representing the stream of interest (GeoJSON).
    gdf_outlet : GeoDataFrame
        GeoDataFrame representing the outlet point (GeoJSON).

    Returns
    -------
    Folium map object.

    Notes
    -----
    This function uses different colors and styles for each layer for better visualization.
    There is also a Layer control panel to show or hide layers.

    """

    lon_min, lat_min, lon_max, lat_max = gdf_bbox.geometry.total_bounds
    delineationMap = folium.Map(location=[(lat_max + lat_min)/2, (lon_min + lon_max)/2], zoom_start=10)

    gdf_riv = gdf_riv.to_crs(4326)
    gdf_bas = gdf_bas.to_crs(4326)
    gdf_riv_clipped = gdf_riv_clipped.to_crs(4326)

    # Convert GeoDataFrames to GeoJSON for display on the map
    gdf_riv_geojson = gdf_riv.to_json()
    gdf_bas_geojson = gdf_bas.to_json()
    gdf_riv_clipped_geojson = gdf_riv_clipped.to_json()
    gdf_outlet_geojson = gdf_outlet.to_json()

    # Draw on Folium map
    Draw(export=True,
         filename='data.geojson',
         draw_options={"polyline": False, "polygon": False,
                       "circle": False, "circlemarker": False}
         ).add_to(delineationMap)

    #  Use folium.GeoJson to add the GeoJSON data to the map
    # Define the style in one command
    style_geom = {'color': 'red',
                  'weight2': 2,
                  'fill': True,
                  'fillColor': 'pink',
                  'fillOpacity': 0.5,}
    folium.GeoJson(gdf_bbox, name="Bounding Box", style_function=lambda x: style_geom).add_to(delineationMap)

    # Add river and basin layers to the map
    folium.GeoJson(gdf_riv_geojson, name="Drainage Network", style_function=lambda x: {
        'color': 'lightblue',
        'fillOpacity': 0.5
    }).add_to(delineationMap)
    folium.GeoJson(gdf_riv_clipped_geojson, name="Stream").add_to(delineationMap)
    folium.GeoJson(gdf_bas_geojson, name="Basin", style_function=lambda x: {
        'color': 'green',
        'fillOpacity': 0.3
    }).add_to(delineationMap)

    folium.GeoJson(gdf_outlet_geojson, name="Outlet Point", show=False).add_to(delineationMap)
    MousePosition(position="topright", separator=" , ",
                  lat_formatter="function(num) {return L.Util.formatNum(num, 3) + ' &deg; ';};",
                  lng_formatter="function(num) {return L.Util.formatNum(num, 3) + ' &deg; ';};",
                  ).add_to(delineationMap)
    # Add a layer control
    folium.LayerControl(position='bottomright', collapsed=False).add_to(delineationMap)

    return delineationMap

########################################################################################################################
################################         Topographic Data         ######################################################
########################################################################################################################

def topographical_data(output_folder, bbox_path, basin_path):
    """
    Generate topographical data including digital elevation map, depression filled elevation map, and flow direction map.
    The resulting datasets are saved in the output folder.

    Parameters
    ----------
    bbox_path : str
        Path to the bounding box GeoJSON file.
    output_folder : str
        Folder where the generated data will be saved.

    Returns
    -------
    tuple
        A tuple containing three raster datasets: elevation map, filled elevation map, and flow direction map.

    Notes
    -----
    This function contains two options for the DEM data:
    1) Copernicus from stitch_dem package, with 30 m * 30 m.
    2) Copernicus from deltares_data server, with 70 m * 30 m. It is only applicable if there is no coverage from the first option. 

    """

    # Get bounding box coordinates from the bounding box polygon
    gdf_bbox = gpd.read_file(bbox_path)
    gdf_basin = gpd.read_file(basin_path)
    lon_min, lat_min, lon_max, lat_max = gdf_bbox.geometry.total_bounds
    bbox=[lon_min, lat_min, lon_max, lat_max]

    # Create a temporal folder to save the layers before projecting them to the corresponding UTM
    temp_folder = os.path.join(output_folder,'topographical_data') 
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

    print("Downloading DEM data..")
    try:
        # Try to download 'glo_30'
        dem_0 = 'glo_30'
        ellipsoidal_hgt = True
        X_0, p_0 = stitch_dem(bbox,
                               dem_0,
                               n_threads_downloading=5,
                               dst_ellipsoidal_height=ellipsoidal_hgt)

        dem_path = os.path.join(temp_folder, 'dem.tif')
        new_profile = p_0.copy()
        new_profile['dtype'] = X_0.dtype.name

        # Create a new GeoTIFF file and write the array to it
        with rasterio.open(dem_path, 'w', **new_profile) as dst:
            dst.write(X_0, 1)

    except NoDEMCoverage as e:
        print("No coverage of 'Copernicus_30m'. Downloading another dataset.")

        # instantiate instance of Data Catalog
        data_catalog = hydromt.DataCatalog(logger=logger_dem, data_libs=["deltares_data"])

        # read MERIT hydro data
        ds = data_catalog.get_rasterdataset("merit_hydro", variables=["elevtn"],
                                            bbox=bbox)

        # read MERIT hydro basin index vector data.
        basin_index = data_catalog.get_geodataframe("merit_hydro_index", bbox=bbox)
        source_list = ["merit_hydro[elevtn]"]
        data_catalog.export_data(
            data_root=temp_folder,
            bbox=bbox,
            source_names=source_list,
        )

        # Alternatively, you can raise the exception again to handle it at a higher level
        raise e
    
    print("DEM map depression filling..")    
    dem_filled_path = os.path.join(temp_folder, "filled_dem.tif")

    # Open the DEM file using rasterio
    with rasterio.open(dem_path) as dem_ds:
        # Read the elevation data from the DEM
        elevation_data = dem_ds.read(1)

        # Call the fill_depressions function
        filled_elevation, flow_directions = pyflwdir.dem.fill_depressions(elevation_data, nodata=-9999)

        # Create a new GeoTIFF file
        profile = dem_ds.profile
        profile.update({'count': 1, 'dtype': 'float32', 'compress': 'lzw', 'nodata': -9999})

        with rasterio.open(dem_filled_path, 'w', **profile) as dst:
            dst.write(filled_elevation, 1)

    dem = rxr.open_rasterio(dem_path, masked=True).squeeze()
    filled_dem = rxr.open_rasterio(dem_filled_path, masked=True).squeeze()

    print("Generating a map identifying depression/sink locations..")
    # identify sinks/depression locations
    sinks = filled_dem - dem

    # Set the zero values in the sinks raster as no data
    sinks = sinks.where(sinks != 0, np.nan)

    sinks_path = os.path.join(temp_folder, 'sinks.tif')

    # Export data to GeoTIFF with no data value set
    sinks.rio.to_raster(sinks_path, nodata=np.nan)

    print("Downloading flow direction map from Deltares hydromt data [Merit Hydro]..")
    data_catalog = hydromt.DataCatalog(logger=logger_dem, data_libs=["deltares_data"])

    # read MERIT hydro data
    ds = data_catalog.get_rasterdataset("merit_hydro", variables=["flwdir"], bbox=bbox)

    source_list = ["merit_hydro[flwdir]"]
    data_catalog.export_data(
        data_root=temp_folder,
        bbox=bbox,
        source_names=source_list,
    )

    # Move the file
    flwdir = os.path.join(temp_folder, "flwdir.tif")
    shutil.move(os.path.join(temp_folder, 'merit_hydro', "flwdir.tif"), flwdir)

    # Specify the path to the folder you want to remove
    folder_path = os.path.join(temp_folder, 'merit_hydro')

    try:
        # Attempt to remove an empty directory using os.rmdir
        os.rmdir(folder_path)
    except OSError as e:
        # If the directory is not empty or other errors occur, use shutil.rmtree
        shutil.rmtree(folder_path)
    except Exception as e:
        print(f"An error occurred: {e}")

    print("Generating a flow direction map clipped on the basin boundary..")
    # Read GeoJSON file
    flwdir_clipped = os.path.join(temp_folder, 'flwdir_basin.tif')

    # Read GeoTIFF file
    with rasterio.open(flwdir) as src:
        # Clip the GeoTIFF using the GeoJSON geometry
        clipped, _ = mask(src, [mapping(gdf_basin.geometry.iloc[0])], crop=True)

        # Get metadata from the original GeoTIFF
        meta = src.meta
    # Update metadata for the clipped GeoTIFF
    meta.update({"driver": "GTiff",
                 "height": clipped.shape[1],
                 "width": clipped.shape[2],
                 "transform": src.window_transform(src.window(*src.bounds))})

    # Write the clipped GeoTIFF to a new file
    with rasterio.open(flwdir_clipped, "w", **meta) as dest:
        dest.write(clipped)

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    # Plot DEM
    im1 = axs[0].imshow(dem, cmap='terrain', extent=dem.rio.bounds(), vmin=dem.min(), vmax=filled_dem.max())
    axs[0].set_title('DEM')
    axs[0].axis('off')
    cbar1 = plt.colorbar(im1, ax=axs[0], orientation='vertical', fraction=0.03, pad=0.1)
    cbar1.set_label('Elevation (m)')
    axs[0].set_xlabel('Longitude (Decimal Degrees)')
    axs[0].set_ylabel('Latitude (Decimal Degrees)')

    # Plot filled DEM
    filled_dem = rxr.open_rasterio(dem_filled_path, masked=True).squeeze()
    im2 = axs[1].imshow(filled_dem, cmap='terrain', extent=filled_dem.rio.bounds(), vmin=dem.min(), vmax=filled_dem.max())
    axs[1].set_title('Filled DEM')
    axs[1].axis('off')
    cbar2 = plt.colorbar(im2, ax=axs[1], orientation='vertical', fraction=0.03, pad=0.1)
    cbar2.set_label('Elevation (m)')
    axs[1].set_xlabel('Longitude (Decimal Degrees)')
    axs[1].set_ylabel('Latitude (Decimal Degrees)')

    # Plot flow direction
    flwdir = rxr.open_rasterio(flwdir, masked=True).squeeze()
    im3 = axs[2].imshow(flwdir, cmap='viridis', extent=flwdir.rio.bounds(), vmin=flwdir.min(), vmax=flwdir.max())
    axs[2].set_title('Flow Direction')
    axs[2].axis('off')
    cbar3 = plt.colorbar(im3, ax=axs[2], orientation='vertical', fraction=0.03, pad=0.1)
    cbar3.set_label('Flow Direction')
    axs[2].set_xlabel('Longitude (Decimal Degrees)')
    axs[2].set_ylabel('Latitude (Decimal Degrees)')

    plt.tight_layout()

    for ax in axs:
        ax.set_xticks(np.linspace(ax.get_xlim()[0], ax.get_xlim()[1], 5))
        ax.set_yticks(np.linspace(ax.get_ylim()[0], ax.get_ylim()[1], 5))
        ax.set_xticklabels(ax.get_xticks(), rotation=45)
        ax.set_yticklabels(ax.get_yticks())

    plt.show()

    #  layer projection
    #####################
    # Define the target UTM zone based on the bounding box
    utm_crs_list = query_utm_crs_info(
        datum_name="WGS 84",
        area_of_interest=AreaOfInterest(
            west_lon_degree=lon_min,
            south_lat_degree=lat_min,
            east_lon_degree=lon_max,
            north_lat_degree=lat_max,
        ),
    )
    utm_crs = CRS.from_epsg(utm_crs_list[0].code)

    # List all GeoTIFF files in the input folder
    tif_files = [f for f in os.listdir(temp_folder) if f.endswith('.tif')]

    for input_tiff_filename in tif_files:
        input_tiff_path = os.path.join(temp_folder, input_tiff_filename)

        # Open the input GeoTIFF file
        with rasterio.open(input_tiff_path) as src:
            # Get the transform and shape of the input raster
            transform, width, height = calculate_default_transform(
                src.crs, utm_crs, src.width, src.height, *src.bounds
            )

            # Define the output GeoTIFF file path
            output_tiff_filename = f"{input_tiff_filename}"
            output_tiff_path = os.path.join(output_folder, output_tiff_filename)

            # Define the profile for the output raster
            dst_profile = src.profile
            dst_profile.update({
                'crs': utm_crs,
                'transform': transform,
                'width': width,
                'height': height
            })

            # Create the output GeoTIFF file
            with rasterio.open(output_tiff_path, 'w', **dst_profile) as dst:
                # Reproject the data from the source to the destination
                reproject(
                    source=rasterio.band(src, 1),
                    destination=rasterio.band(dst, 1),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=utm_crs,
                    resampling=Resampling.nearest  
                )

    print(f"Topographical maps of elevation and flow direction saved to {output_folder}")

    # Delete the temporal folder after projecting all the layer
    shutil.rmtree(temp_folder)

    return dem, filled_dem, flwdir

def correct_dem_with_buildings(output_folder, bbox_path, dem_path, elevation_correction=3.0):
    """
    Corrects a Digital Elevation Model (DEM) by applying an elevation correction to areas of building footprints.

    Parameters
    ----------
    output_folder : str
        Path to the folder where the output files will be saved.
    bbox_path : str
        Path to the GeoJSON file containing the bounding box.
    dem_path : str
        Path to the original DEM file.
    elevation_correction : float, optional
        Elevation correction value (default is 3 meter).

    Returns
    -------
    corrected_dem : GeoTIFF
        Corrected DEM dataset.

    Notes
    -----
    This function generates building footprints, filters out small features of areas less than 250 square meters, resamples the DEM to 2m*2m, and applies an
    elevation correction to areas inside building footprints. The corrected DEM is saved to a new GeoTIFF file.

    """
    # Generate the building footprint
    gdf_bbox = gpd.read_file(bbox_path)
    lon_min, lat_min, lon_max, lat_max = gdf_bbox.geometry.total_bounds
    aoi_geom = {
        "coordinates": [
            [
                [lon_min, lat_max],
                [lon_min, lat_min],
                [lon_max, lat_min],
                [lon_max, lat_max],
                [lon_min, lat_max],
            ]
        ],
        "type": "Polygon",
    }
    aoi_shape = shapely.geometry.shape(aoi_geom)

    output_fn = os.path.join(output_folder,"building_footprints.geojson")

    quad_keys = set()
    for tile in list(mercantile.tiles(lon_min, lat_min, lon_max, lat_max, zooms=9)):
        quad_keys.add(int(mercantile.quadkey(tile)))
    quad_keys = list(quad_keys)
    print(f"The input area spans {len(quad_keys)} tiles: {quad_keys}")

    df = pd.read_csv(
        "https://minedbuildings.blob.core.windows.net/global-buildings/dataset-links.csv"
    )

    idx = 0
    combined_rows = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Download the GeoJSON files for each tile that intersects the input geometry
        tmp_fns = []
        for quad_key in tqdm(quad_keys):
            rows = df[df["QuadKey"] == quad_key]
            if rows.shape[0] == 1:
                url = rows.iloc[0]["Url"]

                df2 = pd.read_json(url, lines=True)
                df2["geometry"] = df2["geometry"].apply(shapely.geometry.shape)

                gdf = gpd.GeoDataFrame(df2, crs=4326)
                fn = os.path.join(tmpdir, f"{quad_key}.geojson")
                tmp_fns.append(fn)
                if not os.path.exists(fn):
                    gdf.to_file(fn, driver="GeoJSON")
            elif rows.shape[0] > 1:
                for i in range(rows.shape[0]):
                    url = rows.iloc[i]["Url"]
                    df2 = pd.read_json(url, lines=True)
                    df2["geometry"] = df2["geometry"].apply(shapely.geometry.shape)
                    gdf = gpd.GeoDataFrame(df2, crs=4326)
                    fn = os.path.join(tmpdir, f"{quad_key}_{i}.geojson")
                    tmp_fns.append(fn)
                    if not os.path.exists(fn):
                        gdf.to_file(fn, driver="GeoJSON")
                #raise ValueError(f"Multiple rows found for QuadKey: {quad_key}")
            else:
                #raise ValueError(f"QuadKey not found in dataset: {quad_key}")
                print(f"QuadKey not found in dataset: {quad_key}")

        # Merge the GeoJSON files into a single file
        for fn in tmp_fns:
            with fiona.open(fn, "r") as f:
                for row in tqdm(f):
                    row = dict(row)
                    shape = shapely.geometry.shape(row["geometry"])

                    if aoi_shape.contains(shape):
                        if "id" in row:
                            del row["id"]
                        row["properties"] = {"id": idx}
                        idx += 1
                        combined_rows.append(row)

    schema = {"geometry": "Polygon", "properties": {"id": "int"}}

    with fiona.open(output_fn, "w", driver="GeoJSON", crs="EPSG:4326", schema=schema) as f:
        f.writerecords(combined_rows)                    

    # Remove all the features with an area less than 250 m^2
    gdf = gpd.read_file(output_fn)

    # Check the CRS of the original GeoDataFrame
    print("Original CRS:", gdf.crs)

    # Reproject the GeoDataFrame to a projected CRS
    gdf = gdf.to_crs(epsg=3857)

    # Calculate the area for each polygon and create a new column 'area' in the GeoDataFrame
    gdf['area'] = gdf.geometry.area

    # Filter out features with an area less than 250 m²
    gdf_filtered = gdf[gdf['area'] >= 250]

    # Drop the 'area' column if you no longer need it
    gdf_filtered = gdf_filtered.drop(columns=['area'])

    # Clean the geometries
    gdf_filtered = gdf_filtered.set_geometry(gdf_filtered.geometry.buffer(0))

    # Save the filtered GeoDataFrame to a new GeoJSON file
    output_file_path = os.path.join(output_folder, 'filtered_buildings.geojson')
    gdf_filtered.to_file(output_file_path, driver='GeoJSON')

    # Resampling the DEM to 2m * 2m
    with rasterio.open(dem_path) as src:
        # Resample data to target shape
        data = src.read(
            out_shape=(
                src.count,
                int(src.height * 15),
                int(src.width * 15)
            ),
            resampling=Resampling.bilinear
        )

        # Scale image transform
        transform = src.transform * src.transform.scale(
            (src.width / data.shape[-1]),
            (src.height / data.shape[-2])
        )

        # Update the metadata
        profile = src.profile
        profile.update({
            'driver': 'GTiff',
            'height': data.shape[1],
            'width': data.shape[2],
            'transform': transform
        })

        # Write the resampled data to a new file
        dem_resampled= os.path.join(output_folder, 'dem_2m_resampled.tif')
        with rasterio.open(dem_resampled, 'w', **profile) as dst:
            dst.write(data)

    # Correct the DEM accordingly
    # Read the GeoTIFF file (DEM)
    with rasterio.open(dem_resampled) as dem_src:
        dem_data = dem_src.read(1)  # Assuming a single-band DEM

        # Read the GeoJSON file (building polygons)
        buildings_gdf = gpd.read_file(output_fn)

        # Reproject the GeoJSON to match the CRS of the DEM
        buildings_gdf = buildings_gdf.to_crs(dem_src.crs)

        # Convert dem_src.bounds to a GeoDataFrame with a single polygon
        dem_bounds_gdf = gpd.GeoDataFrame(
            geometry=[box(*dem_src.bounds)],
            crs=dem_src.crs
        )

        # Check if the building geometries overlap with the raster
        if not buildings_gdf.geometry.intersects(dem_bounds_gdf.geometry.iloc[0]).any():
            raise ValueError("Building geometries do not overlap with the raster.")

        # Generate a GeoJSON-like geometry for buildings
        building_geometries = [building["geometry"] for _, building in buildings_gdf.iterrows()]

        # Create a mask for areas inside building footprints
        building_mask = geometry_mask(building_geometries, out_shape=dem_data.shape, transform=dem_src.transform, invert=True)

        # Apply elevation correction only to areas inside building footprints
        dem_data[building_mask] += elevation_correction

        # Write the corrected DEM to a new file
        output_file = os.path.join(output_folder, 'corrected_dem.tif')
        with rasterio.open(output_file, 'w', **dem_src.profile) as corrected_dem:
            corrected_dem.write(dem_data, 1)

    return corrected_dem

########################################################################################################################
################################          Grid Generation         ######################################################
########################################################################################################################

def generate_mesh(output_folder, basin_path, basin_proj_path, flwdir_path, block_size_x= 30, block_size_y= 30):
    """
    Generate a two directional mesh based on the given horizontal and vertical resolution 
    and inclined based on the basin average flow direction.

    Parameters
    ----------
    block_size_x : float
        Size of the grid block in the x-direction in meters.
    block_size_y : float
        Size of the grid block in the y-direction in meters.
    basin_path : str
        Path to the basin GeoJSON file.
    basin_proj_path : str
        Path to the UTM projected basin GeoJSON file.
    flwdir_path : str
        Path to the flow direction raster file.
    output_folder : str
        Path to the folder where the output NetCDF file will be saved.

    Returns
    -------
    mesh2d : Mesh2D
        A UTM projected 2D mesh object.

    Notes
    -----
    This function can read bounding box and basin file. Thus, the it can generate basin shape or rectangular 2D mesh.
    The resulting mesh is saved in the NetCDF format.

    """

    # ---- Read the basin Data----
    ##############################

    gdf_proj = gpd.read_file(basin_proj_path)
    gdf = gpd.read_file(basin_path)

    # Get bounding box coordinates from the bounding box polygon
    lon_min, lat_min, lon_max, lat_max = gdf.geometry.total_bounds
    polygon = gdf_proj.geometry.iloc[0]

    # Extract polygon coordinates
    exterior_coords = np.array(polygon.exterior.coords.xy).T

    # Calculate origin coordinates
    origin_x = np.min(exterior_coords[:, 0])
    origin_y = np.min(exterior_coords[:, 1])

    # Save coordinates as separate arrays
    node_x = exterior_coords[:, 0]
    node_y = exterior_coords[:, 1]


    # Save the arrays using np.savez
    geometry_list = GeometryList(node_x, node_y)

    # -- Calculate the mean Flwdir--
    ##############################
    # Open the TIFF file using rasterio
    with rasterio.open(flwdir_path) as src:
        # Read the flow direction data as a NumPy array
        flow_direction_map = src.read(1, masked=True)

        # Define the flow direction values and corresponding angles
        direction_angles = {2: 0, 4: 45, 8: 90, 16: 135, 32: 180, 64: 225, 128: 270, 1: 315}

        # Calculate flow direction angles for each cell
        cell_angles = np.vectorize(direction_angles.get)(flow_direction_map)

        # Calculate the average angle
        average_angle = np.mean(cell_angles)

    if average_angle >= 0 and average_angle <= 90:
        angle = average_angle
    elif average_angle > 90 and average_angle < 270:
        angle = average_angle - 180
    else:
        angle = average_angle - 360

    # ------- Grid Parameters------
    ##############################

    make_grid_parameters = MakeGridParameters()
    make_grid_parameters.angle = angle
    make_grid_parameters.origin_x = origin_x
    make_grid_parameters.origin_y = origin_y
    make_grid_parameters.block_size_x = block_size_x
    make_grid_parameters.block_size_y = block_size_y

  
    # ----- Generate the Grid-------
    ##############################

    mk = MeshKernel(projection=meshkernel.ProjectionType.CARTESIAN)
    mk.curvilinear_compute_rectangular_grid_from_polygon(make_grid_parameters, geometry_list)
    curvilineargrid = mk.curvilineargrid_get()
    mk.curvilinear_convert_to_mesh2d()
    mesh2d = mk.mesh2d_get()

    fig, ax = plt.subplots()
    ax.axis('equal')
    mesh2d.plot_edges(ax)
  
    # ------- Define the CRS--------
    ##############################

    # Define the target UTM zone based on the bounding box
    utm_crs_list = query_utm_crs_info(
        datum_name="WGS 84",
        area_of_interest=AreaOfInterest(
            west_lon_degree=lon_min,
            south_lat_degree=lat_min,
            east_lon_degree=lon_max,
            north_lat_degree=lat_max,
        ),
    )
    utm_crs = CRS.from_epsg(utm_crs_list[0].code)
    utm_crs_string = utm_crs.to_string()


    # -- Save the mesh into NetCDF--
    ##############################

    xu_grid = xu.Ugrid2d.from_meshkernel(mesh2d, projected= True, crs=utm_crs)
    
    #convert 0-based to 1-based indices for connectivity variables like face_node_connectivity
    xu_grid_ds = xu_grid.to_dataset()
    xu_grid_ds = xr.decode_cf(xu_grid_ds) #decode_cf is essential since it replaces fillvalues with nans
    ds_idx = xu_grid_ds.filter_by_attrs(start_index=0)
    for varn_conn in ds_idx.data_vars:
        xu_grid_ds[varn_conn] += 1 #from startindex 0 to 1 (fillvalues are now nans)
        xu_grid_ds[varn_conn].attrs["start_index"] += 1
        xu_grid_ds[varn_conn].encoding["_FillValue"] = -1 #can be any value <=0, but not 0 is currently the most convenient for proper xugrid plots.
    
    # convert to uds and add attrs and crs
    xu_grid_uds = xu.UgridDataset(xu_grid_ds)
    
    xu_grid_uds = xu_grid_uds.assign_attrs({'Conventions': 'CF-1.8 UGRID-1.0 Deltares-0.10', 
                                          'institution': 'Deltares',
                                          'references': 'https://www.deltares.nl',
                                          'source': f'Created with meshkernel {meshkernel.__version__}, xugrid {xu.__version__}',
                                          'EPSG_code': utm_crs_string,
                                          'history': 'Created on %s, %s'%(dt.datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z'),getpass.getuser()), #add timezone
                                          })
    xu_grid_uds.ugrid.set_crs(utm_crs)
    # write xugrid grid to netcdf
    netfile = os.path.join(output_folder, 'mesh2d_net.nc')
    xu_grid_uds.ugrid.to_netcdf(netfile)
    
    print(f"2-dimentional mesh saved to {netfile}")

    return xu_grid_uds

########################################################################################################################
################################           Roughness Map          ######################################################
########################################################################################################################

def roughness_map(output_folder, bbox_path, csv_file_path= 'roughness_reclass.csv'):

    """
    Generate a roughness map based on land use map and a CSV classification file.

    Parameters
    ----------
    bbox_path : str
        Path to the bounding box GeoJSON file.
    csv_file_path : str
        Path to the CSV file containing land use classes ID and roughness values.
    output_folder : str
        Path to the folder where the output roughness map will be saved.

    Returns
    -------
    roughness : GeoTIFF
        A roughness map.

    Notes
    -----
    This function reads the bounding box, then exports ESA land use data from deltares_data server, with a 10 m * 10 m  resolution.
    The user should use the example csv file and change the defualt roughness values based on their expected values.
    Please do not change the first three columns, only change the fourth column of the CSV so that you can have a smooth process.

    """
    # Get bounding box coordinates from the bounding box polygon
    gdf = gpd.read_file(bbox_path)
    lon_min, lat_min, lon_max, lat_max = gdf.geometry.total_bounds

    data_catalog = hydromt.DataCatalog(
        logger=logger_roughness,
        data_libs=["deltares_data"],
    )
    source_list = ["esa_worldcover"]
    bbox = [lon_min, lat_min, lon_max, lat_max]
    data_catalog.export_data(
        data_root=output_folder,
        bbox=bbox,
        source_names=source_list,
    )
    # Define the target UTM zone based on the bounding box
    utm_crs_list = query_utm_crs_info(
        datum_name="WGS 84",
        area_of_interest=AreaOfInterest(
            west_lon_degree=lon_min,
            south_lat_degree=lat_min,
            east_lon_degree=lon_max,
            north_lat_degree=lat_max,
        ),
    )
    utm_crs = CRS.from_epsg(utm_crs_list[0].code)

    # Read CSV file
    reclass_dict = {}
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # Skip the header row
        next(reader)

        for row in reader:
            # Check if the row has enough columns
            if len(row) >= 4:  # Ensure there are at least 4 columns (0-based indexing)
                landuse = int(row[2])  # Third column (index 2) for landuse
                roughness_manning = float(row[3])  # Fourth column (index 3) for roughness-manning
                reclass_dict[landuse] = roughness_manning
            else:
                print(f"Warning: Row skipped due to insufficient columns - {row}")

    # Open raster dataset using rasterio
    input_raster_path = os.path.join(output_folder, "esa_worldcover.tif")
    with rasterio.open(input_raster_path) as raster_ds:
        xsize = raster_ds.width
        ysize = raster_ds.height

        # Create output raster dataset
        reclassified = os.path.join(output_folder, 'roughness4326.tif')
        profile = raster_ds.profile
        profile.update({'dtype': 'float32'})
        with rasterio.open(reclassified, 'w', **profile) as roughness:
            chunk_size=100
            for yoff in range(0, ysize, chunk_size):
                for xoff in range(0, xsize, chunk_size):
                    xsize_chunk = min(chunk_size, xsize - xoff)
                    ysize_chunk = min(chunk_size, ysize - yoff)

                    window = Window(xoff, yoff, xsize_chunk, ysize_chunk)
                    raster_array = raster_ds.read(1, window=window, out_shape=(ysize_chunk, xsize_chunk))
                    reclassified_array = np.vectorize(lambda x: reclass_dict.get(x, x))(raster_array)
                    roughness.write(reclassified_array, 1, window=window)


        # Open the input GeoTIFF file
    with rasterio.open(reclassified) as src:
        # Get the transform and shape of the input raster
        transform, width, height = calculate_default_transform(
            src.crs, utm_crs, src.width, src.height, *src.bounds
        )

        # Define the profile for the output raster
        dst_profile = src.profile
        dst_profile.update({
            'crs': utm_crs,
            'transform': transform,
            'width': width,
            'height': height
        })
        # Create the output GeoTIFF file
        reclassified_projected = os.path.join(output_folder, 'roughness.tif')
        with rasterio.open(reclassified_projected, 'w', **dst_profile) as dst:
            # Reproject the data from the source to the destination
            reproject(
                source=rasterio.band(src, 1),
                destination=rasterio.band(dst, 1),
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=utm_crs,
                resampling=Resampling.nearest  # You can choose a different resampling method if needed
            )
    print(f"Roughness map saved to {reclassified_projected}")  

    os.remove(reclassified)  # Delete the geographic GeoTIFF file
    return roughness

########################################################################################################################
################################         Infiltration Maps        ######################################################
########################################################################################################################

def infiltration_map(output_folder, bbox_path, lulc_path, csv_path = 'infiltration_reclass.csv'):
    """
    Generate infiltration maps based on soil and land use classifications.

    Parameters
    ----------
    bbox_path : str
        Path to the bounding box GeoJSON file.
    lulc_path : str
        Path to the land use and land cover (LULC) GeoTIFF file.
    csv_path : str
        Path to the CSV file containing infiltration information.
    output_folder : str
        Path to the folder where the output infiltration maps will be saved.

    Returns
    -------
    dst : GeoTIFF
        Raster object representing the generated infiltration map.

    Notes
    -----
    This function reads the bounding box, exports soil data, calculates infiltration maps based on
    soil and land use classifications, and saves the minimum, maximum, and decrease rate infiltration maps.
    The resulted maps have the resolution of the LULC map.

    """
    # Read the bounding box file
    gdf_bbox = gpd.read_file(bbox_path)

    # Get bounding box coordinates from the bounding box polygon
    lon_min, lat_min, lon_max, lat_max = gdf_bbox.geometry.total_bounds
    bbox=[lon_min, lat_min, lon_max, lat_max]


    # Download artifacts for the Piave basin to `~/.hydromt_data/`.
    data_catalog = hydromt.DataCatalog(logger=logger_infilt, data_libs=["deltares_data"])

    # Download soilgrids data
    for prefix in ["clyppt", "sltppt"]:
        for i in range(1, 7):
            source_name = f"soilgrids[{prefix}_sl{i}]"
            
            # Export data for the current source
            data_catalog.export_data(
                data_root=os.path.join(output_folder, prefix),
                bbox=bbox,
                source_names=[source_name],
            )

    # Accumulate and save the data
    for prefix in ["clyppt", "sltppt"]:
        # List of input TIFF files
        input_files = glob.glob(os.path.join(output_folder, f"{prefix}/soilgrids/*.tif"))

        if not input_files:
            print(f"No TIFF files found for {prefix}.")
        else:
            # Read the first TIFF file to get dimensions, CRS, transform, and NoData value information
            with rasterio.open(input_files[0]) as src:
                first_tiff = src.read(1)
                crs = src.crs
                transform = src.transform  # Get the transform from the input file
                count = src.count  # Get the band count from the input file
                nodata = src.nodata  # Get the NoData value from the input file

            # Initialize an accumulator array
            total_sum = np.zeros_like(first_tiff, dtype=np.float32)  # Adjust dtype as needed

            # Loop through each TIFF file and accumulate the sum
            for file_path in input_files:
                with rasterio.open(file_path) as src:
                    img = src.read(1)
                    img = img.astype(np.float32)  # Convert to float32
                    # Set NoData values to NaN (Not a Number)
                    img[img == nodata] = np.nan
                    total_sum += img

            # Divide the summed raster values by the number of files
            total_sum /= len(input_files)

            # Save the divided TIFF as a new file with the same CRS and geospatial information
            output_file = os.path.join(output_folder, f"{prefix}.tif")
            with rasterio.open(output_file, 'w', driver='GTiff', width=total_sum.shape[1], height=total_sum.shape[0],
                               dtype=np.float32, crs=crs, transform=transform, count=count) as dst:
                # Set NoData value in the output TIFF file
                dst.nodata = np.nan
                dst.write(total_sum, 1)

    # Step 3: Create sand layer
    clay = rxr.open_rasterio(os.path.join(output_folder, "clyppt.tif"), masked=True).squeeze()
    silt = rxr.open_rasterio(os.path.join(output_folder, "sltppt.tif"), masked=True).squeeze()
    sand = 100 - (clay + silt)

    sand_filename = 'sand.tif'
    sand_path = os.path.join(output_folder, sand_filename)

    # Export data to GeoTIFF with no data value set
    sand.rio.to_raster(sand_path, nodata=np.nan)

    def USDA_classify_soil(sand, silt, clay):
        if sand >= 86 and silt <= 14 and clay <= 10:
            return "Sands"
        elif 70 <= sand < 86 and silt <= 30 and clay <= 15:
            return "Loamy sand"
        elif 50 <= sand < 70 and silt <= 50 and clay <= 20:
            return "Sandy loam"
        elif 23 <= sand < 52 and 28 <= silt <= 50 and clay <= 27:
            return "Loam"
        elif sand <= 50 and 74 <= silt <= 88 and clay <= 27:
            return "Silty loam"
        elif sand <= 20 and 88 <= silt <= 100 and clay <= 12:
            return "Silt"
        elif 20 <= sand < 45 and 15 <= silt <= 52 and 27 <= clay <= 40:
            return "Clay loam"
        elif 45 <= sand < 80 and silt <= 28 and 20 <= clay <= 35:
            return "Sandy clay loam"
        elif sand <= 20 and 40 <= silt <= 73 and 27 <= clay <= 40:
            return "Silty clay loam"
        elif 45 <= sand < 65 and silt <= 20 and 35 <= clay <= 55:
            return "Sandy clay"
        elif sand <= 20 and 40 <= silt <= 60 and 40 <= clay <= 60:
            return "Silty clay"
        elif sand <= 45 and silt <= 40 and 40 <= clay <= 100:
            return "Clay"
        else:
            return "Unknown"

    sand_raster = rasterio.open(os.path.join(output_folder, "sand.tif"))
    silt_raster = rasterio.open(os.path.join(output_folder, "sltppt.tif"))
    clay_raster = rasterio.open(os.path.join(output_folder, "clyppt.tif"))

    # Step 2: Extract pixel values as numpy arrays
    sand = sand_raster.read(1)
    silt = silt_raster.read(1)
    clay = clay_raster.read(1)

    # Step 4: Apply the classify_soil function to each pixel and assign unique integer codes
    classes_mapping = {
        'Sands': 1,
        'Loamy sand': 2,
        'Sandy loam': 3,
        'Loam': 4,
        'Silty loam': 5,
        'Silt': 6,
        'Clay loam': 7,
        'Sandy clay loam': 8,
        'Silty clay loam': 9,
        'Sandy clay': 10,
        'Silty clay': 11,
        'Clay': 12,
        'Unknown': 0
    }

    rows, cols = sand.shape
    result_matrix = np.zeros((rows, cols), dtype=np.uint8)

    for row in range(rows):
        for col in range(cols):
            textural_class = USDA_classify_soil(sand[row, col], silt[row, col], clay[row, col])
            result_matrix[row, col] = classes_mapping[textural_class]

    # Step 5: Save the result_matrix as a raster file
    output_profile = sand_raster.profile
    output_profile.update(dtype=rasterio.uint8, count=1)

    soil_path = os.path.join(output_folder, "soil_type.tif")

    with rasterio.open(soil_path, 'w', **output_profile) as dst:
        dst.write(result_matrix, 1)

    # Open raster files
    lulc_dataset = rasterio.open(lulc_path)
    soil_dataset = rasterio.open(soil_path)

    #Get resolusion
    gt = lulc_dataset.transform
    pixelSize = gt[0]

    # Merge the datasets using the virtual dataset for the LULC data
    datasets = [lulc_dataset, soil_dataset]
    merged, out_trans = merge(datasets)

    # Output path for the merged result with separate bands
    output_path = os.path.join(output_folder, 'lulc_soil.tif')

    # Update metadata for the merged file with separate bands
    out_meta = lulc_dataset.meta.copy()
    out_meta.update({
        "driver": "GTiff",
        "count": len(datasets),  # Set the number of bands
        "transform": out_trans
    })

    # Write the merged dataset with separate bands to a new file
    with rasterio.open(output_path, "w", **out_meta) as dest:
        for i in range(len(datasets)):
            dest.write(datasets[i].read(1), i + 1)  # Write each dataset to a separate band

    # Close the opened datasets
    lulc_dataset.close()
    soil_dataset.close()

    with rasterio.open(output_path) as src:
        l_affine = src.transform
        soil_ds = src.read(1)
        lulc_ds = src.read(2)
        
    if lulc_ds is None or soil_ds is None:
        print("Error: Unable to open raster files")

    csv_file = pd.read_csv(csv_path)

    min_inf_values = []
    max_inf_values = []
    dr_values = []

    # Use tqdm_bar to create a progress bar for the outer loop
    for i in tqdm_bar(range(soil_ds.shape[0]), desc="Rows"):
        # Initialize empty lists for each row
        row_min_inf = []
        row_max_inf = []
        row_dr = []

        for j in range(soil_ds.shape[1]):
            lc = soil_ds[i, j]
            st = lulc_ds[i, j]

            # Use NumPy vectorization to find the matching index
            idx = csv_file[(csv_file['lulc'] == lc) & (csv_file['soil'] == st)].index

            if not idx.empty:
                # Access individual elements using indexing
                row_min_inf.append(csv_file.iloc[idx, 3].values[0])
                row_max_inf.append(csv_file.iloc[idx, 2].values[0])
                row_dr.append(csv_file.iloc[idx, 4].values[0])
            else:
                # Handle the case where no match is found
                row_min_inf.append(None)
                row_max_inf.append(None)
                row_dr.append(None)

        # Append the lists for the current row to the main lists
        min_inf_values.append(row_min_inf)
        max_inf_values.append(row_max_inf)
        dr_values.append(row_dr)

    # Convert the lists to NumPy arrays
    min_inf = np.array(min_inf_values)
    max_inf = np.array(max_inf_values)
    dr = np.array(dr_values)

    output_min_inf_path = os.path.join(output_folder, "infil_min.tif")
    output_max_inf_path = os.path.join(output_folder,"infil_max.tif")
    output_dr_path = os.path.join(output_folder,"decrease_rate.tif")

    pixel_size = pixelSize
    # Calculate the dimensions of the output image
    output_height = min_inf.shape[0]
    output_width = min_inf.shape[1]

    # Retrieve the CRS of the source dataset
    source_crs = src.crs
    # Define the profile for the output files with the correct CRS
    profile = {
        'driver': 'GTiff',
        'dtype': 'float64',
        'count': 1,
        'height': output_height,
        'width': output_width,
        'crs': source_crs,  # Set the CRS to match the input data's CRS
        'transform': src.transform
    }
    # Save the minimum infiltration map
    with rasterio.open(output_min_inf_path, 'w', **profile) as dst:
        dst.write(min_inf, 1)

    # Save the  maximum infiltration map
    with rasterio.open(output_max_inf_path, 'w', **profile) as dst:
        dst.write(max_inf, 1)

        # Save the decrease rate map
    with rasterio.open(output_dr_path, 'w', **profile) as dst:
        dst.write(dr, 1)
    
    return dst

########################################################################################################################
################################      Evapotranspiration Data     ######################################################
########################################################################################################################

def evaporation(output_folder, startDate, endDate, bbox_path):
    """
    Calculate daily and hourly evaporation using the Penman-Monteith method.
    It saves the output as CSV and GeoTIFF files.

    Parameters
    ----------
    startDate : str
        Start date of the time period in the format 'YYYY-MM-DD'.
    endDate : str
        End date of the time period in the format 'YYYY-MM-DD'.
    bbox_path : str
        Path to the bounding box GeoJSON file.
    output_folder : str
        Path to the folder where the output files will be saved.

    Returns
    -------
    evap : xarray.Dataset
        Xarray dataset containing calculated evaporation values.

    """
    # Get bounding box coordinates from the bounding box polygon
    gdf = gpd.read_file(bbox_path)
    lon_min, lat_min, lon_max, lat_max = gdf.geometry.total_bounds
    
    # Specify Deltares' global data server:
    data_catalog = hydromt.DataCatalog(logger=logger_meteo, data_libs=["deltares_data"])
    bbox = [lon_min-0.25, lat_min-0.25, lon_max+0.25, lat_max+0.25]
    ERA5_hourly = data_catalog.get_rasterdataset("era5_hourly", bbox=bbox, time_tuple=[startDate, endDate])
    
    # Initialize data:
    T = ERA5_hourly["temp"]                            # C
    d2m = ERA5_hourly["temp_dew"]                      # C
    R = ERA5_hourly["ssr"] / (2.45 * 10**6)            # mm/hr
    P = ERA5_hourly["press_msl"] / 1000                # KPa
    u10 = ERA5_hourly["wind10_u"]                      # m/s
    v10 = ERA5_hourly["wind10_v"]                      # m/s

    es = 0.6108 * np.exp(17.27 * T/ (237.3 + T))       # KPa
    delta = 4098 * es / (237.3 + T)**2                 # KPa/C
    Y = 2.501 - 0.002361 * T                           # MJ/Kg
    gamma = 0.0016286 * P / Y                          # KPa/C
    U = np.sqrt(u10 ** 2 + v10 ** 2)                   # m/s
    es = 0.6108 * np.exp(17.27 * T / (T + 237.3))      # KPa
    e = 0.6108 * np.exp(17.27 * d2m / (d2m + 237.3))   # KPa
    D = es - e                                         # KPa

    evap = ((delta * R)/(delta + gamma) + (6.43 * gamma * D * (1 + 0.53 * U))/(Y * (delta + gamma)))
    evap_mean = evap.mean(["latitude", "longitude"])
    evap_daily = evap.resample(time="1D").sum(skipna=True)
    evap_daily_mean = evap_mean.resample(time="1D").sum(skipna=True)

    # Save the result to a CSV file
    df_daily = evap_daily_mean.to_dataframe("ETp")
    df_daily.to_csv(os.path.join(output_folder,'ETp_daily.csv'))
    df_hourly = evap_mean.to_dataframe("ETp")
    df_hourly.to_csv(os.path.join(output_folder,'ETp_hourly.csv'))

    # Save the result to a GeoTIFF file
    daily_output = os.path.join(output_folder,'ETp_daily.tif')
    evap_daily.rio.to_raster(daily_output, nodata=np.nan)
    hourly_output = os.path.join(output_folder,'ETp_hourly.tif')
    evap.rio.to_raster(hourly_output, nodata=np.nan)

    return evap

########################################################################################################################
################################           Rainfall Data          ######################################################
########################################################################################################################

def disaggregate_precipitation(output_folder, rainfall_volume, distribution_type='normal', interval_size=24):
    """
    Disaggregate daily precipitation into hourly values based on the specified distribution type.

    Parameters
    ----------
    output_folder : str
        Path to the folder where the output files will be saved.
    rainfall_volume : float
        Total observed rainfall volume.
    distribution_type : str, optional
        Type of distribution for disaggregation ('normal' by default).
        The rainfall in this function can have one of these distributions: uniform, normal, lognormal, weibull, GEV, or gamma.
    interval_size : int, optional
        Size of the rainfall interval to disaggregate the rainfall volume (default is 24 hour).

    Returns
    -------
    hourly_values : Array
        Array of disaggregated precipitation values.

    Notes
    -----
    This function disaggregates precipitation data into smaller time interval values using different distribution types,
    saves the results to a CSV file, and displays a plot. It can be used to disaggregate from daily to hourly, hourly to minutes, 
    from monthly to daily or any other time interval.

    """
    # Check if the specified distribution type is valid
    allowed_distribution_types = ['uniform', 'normal', 'gamma', 'weibull', 'GEV', 'lognormal']
    if distribution_type not in allowed_distribution_types:
        raise ValueError(f"Invalid distribution_type. Choose one of {', '.join(allowed_distribution_types)}.") 
       
    # Generate hourly values based on the specified distribution type
    if distribution_type == 'uniform':
        # Uniform distribution
        hourly_values = np.full(interval_size, rainfall_volume / interval_size)
    elif distribution_type == 'normal':
        # Normal distribution
        mean = interval_size / 2
        std_dev = interval_size / 8
        t = np.linspace(0, 1, interval_size)
        pdf_values = norm.pdf(t, loc=mean / interval_size, scale=std_dev / interval_size)
        hourly_values = pdf_values / np.sum(pdf_values) * rainfall_volume
    elif distribution_type == 'gamma':
        # Gamma distribution
        shape = interval_size / 12
        scale = interval_size / 4
        t = np.linspace(0, 1, interval_size)
        pdf_values = gamma.pdf(t, shape, scale=scale / interval_size)
        hourly_values = pdf_values / np.sum(pdf_values) * rainfall_volume
    elif distribution_type == 'weibull':
        # Weibull distribution
        shape = interval_size / 12
        scale = interval_size / 4
        t = np.linspace(0, 1, interval_size)
        pdf_values = weibull_min.pdf(t, c=shape, scale=scale / interval_size)
        hourly_values = pdf_values / np.sum(pdf_values) * rainfall_volume
    elif distribution_type == 'GEV':
        # Generalized Extreme Value (GEV) distribution
        loc = interval_size / 2
        scale = interval_size / 8
        shape = interval_size / 240
        t = np.linspace(0, 1, interval_size)
        pdf_values = genextreme.pdf(t, loc=loc / interval_size, scale=scale / interval_size, c=-shape)
        hourly_values = pdf_values / np.sum(pdf_values) * rainfall_volume
    elif distribution_type == 'lognormal':
        # Lognormal distribution
        mean_log = interval_size / 12
        std_dev_log = interval_size / 48
        t = np.linspace(0, 1, interval_size)
        pdf_values = lognorm.pdf(t, s=std_dev_log, scale=np.exp(mean_log - 0.5 * std_dev_log**2))
        hourly_values = pdf_values / np.sum(pdf_values) * rainfall_volume

    # Create a DataFrame with hourly rainfall data, including an index column
    hourly_precipitation = pd.DataFrame({
        'Distributed Hourly Rainfall': hourly_values
    })

    # Save the resulting time series to a CSV file
    pcp_path = os.path.join(output_folder, f'hourly_precipitation_{distribution_type}.csv')
    hourly_precipitation.to_csv(pcp_path)

    # Plotting the result
    plt.figure()
    ax = plt.gca()
    hourly_precipitation.plot(ax=ax, label='Distributed Rainfall', color='blue')
    ax.scatter([], [], color='red', marker=' ', label=f'Total Observed Rainfall = {rainfall_volume} mm')
    ax.set_xlabel('Time')
    ax.set_ylabel('Rainfall')
    plt.legend()
    plt.show()
    print(f"Disaggregated precipitation saved to {pcp_path}")
    return hourly_values

########################################################################################################################
################################        MDU File Generation       ######################################################
########################################################################################################################

def mdu_file(output_folder, rainfall_file, startDate, startTime = '00:00:00', time_unit = 'hr', rainfall_unit= 'mm/hr'):
    """
    Generate a D-Flow FM model files with specified initial conditions, parameters, and boundary conditions.

    Parameters
    ----------
    output_folder : str
        Path to the folder where the D-Flow FM model files will be saved.
    rainfall_file : str
        Path to the CSV file containing rainfall time series data.
        It should contain two columns, the first one for time and the second for the rainfall
    startDate : str
        Start date of the simulation (Format: YYYY-MM-DD).
    startTime : str, optional
        Start time of the simulation (default is '00:00:00').
    time_unit : str, optional
        Unit of time used in the simulation (default is 'hr').
    rainfall_unit : str, optional
        Unit of rainfall used in the simulation (default is 'mm/hr').

    Returns
    -------
    fm : FMModel
        D-Flow FM model instance.
    """
    
    # Create empty D-Flow FM model
    fm = FMModel()
    # Assign filepath to the D-Flow FM model
    fm.filepath = os.path.join(output_folder,'FlowFM.mdu')
    fm.save()

    # Define the mesh2d file
    mesh2d = Mesh2d()
    fm.geometry.netfile.network._mesh2d = mesh2d
    fm.geometry.netfile.filepath = "mesh2d_net.nc"

    # Create initial field file
    ini_field = IniFieldModel()
    ini_field.filepath = 'inifield.ini'
    ini_field.initial = InitialField(quantity='bedlevel',
                                    datafile='dem.tif', 
                                    datafiletype=DataFileType.geotiff,
                                    interpolationMethod = InterpolationMethod.triangulation,
                                    locationType = LocationType.twod)
    parameters = []
    parameters.append(ParameterField(
        quantity='frictioncoefficient',
        dataFile='roughness.tif',
        dataFileType=DataFileType.geotiff,
        interpolationMethod=InterpolationMethod.triangulation,
        locationType=LocationType.twod
    ))

    parameters.append(ParameterField(
        quantity='HortonMaxInfCap',
        dataFile='infil_max.tif',
        dataFileType=DataFileType.geotiff,
        interpolationMethod=InterpolationMethod.triangulation,
        locationType=LocationType.twod
    ))

    parameters.append(ParameterField(
        quantity='HortonMinInfCap',
        dataFile='infil_min.tif',
        dataFileType=DataFileType.geotiff,
        interpolationMethod=InterpolationMethod.triangulation,
        locationType=LocationType.twod
    ))

    parameters.append(ParameterField(
        quantity='HortonDecreaseRate',
        dataFile='decrease_rate.tif',
        dataFileType=DataFileType.geotiff,
        interpolationMethod=InterpolationMethod.triangulation,
        locationType=LocationType.twod
    ))

    ini_field.parameter = parameters
    fm.geometry.inifieldfile = ini_field

    #Gnerate boundary condition file
    bc_file = ForcingModel()
    bc_file.filepath = 'rainfall.bc'
    rainfall = pd.read_csv(rainfall_file, sep=',', skiprows=1, header=None, names=['', 'Distributed Hourly Rainfall'])

    bc = TimeSeries(
        name='global',
        function='timeseries',
        timeinterpolation=TimeInterpolation.linear,
        quantityunitpair=[
            QuantityUnitPair(quantity='time', unit=f'{time_unit} since {startDate} {startTime}'),
            QuantityUnitPair(quantity='rainfall_rate', unit=f'{rainfall_unit}')],
        datablock=[[time, dis] for time, dis in zip(rainfall[''], rainfall['Distributed Hourly Rainfall'])])
    bc_file.forcing.append(bc)

    ext_model = ExtModel()   
    fm.external_forcing.extforcefilenew = ext_model
    ext_upstream = Meteo(
        quantity = 'rainfall_rate',
        forcingfile = bc_file,
        forcingFileType= 'bcAscii',)

    ext_model.boundary.append(ext_upstream)

    # Save the mdu with the changes
    fm.general.autostart = AutoStartOption.no # This is a workaround for a bug in hydrolib-core 0.3.1
    fm.save(recurse=True)
    file_path = os.path.join(output_folder, 'FlowFM.mdu')
    new_line = "[grw]\nInfiltrationmodel                 = 4      # Infiltration method (0: No infiltration, 1: Interception layer, 2: Constant infiltration capacity, 3: model unsaturated/saturated (with grw), 4: Horton))"

    # Open the file in append mode to add content at the end
    with open(file_path, 'a') as file:
        # Write the new line to the file
        file.write(new_line)
    return fm