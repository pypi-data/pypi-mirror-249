import pandas as pd
import geopandas as gpd
import requests
from io import BytesIO
import pickle
from pathlib import Path
import osmnx as ox
import os
import folium
import sys


def load_locations_from_csv(file_path):
    """
    Load locations data from a CSV file.
    Parameters:
    file_path (str): Path to the CSV file.
    Returns:
    pandas.DataFrame: Dataframe containing the locations data.
    """
    locations_df = pd.read_csv(file_path)

    # Check the data type of the 'Population' column and convert it to numeric if not already
    if not pd.api.types.is_numeric_dtype(locations_df['Population']):
        locations_df['Population'] = pd.to_numeric(locations_df['Population'].str.replace(',', ''), errors='coerce')

    return locations_df


def preprocess_locations_data(locations_df):
    """
    Identify rows with NaN values and drop them. Also, prepare data for heatmap layer.
    """
    nan_population = locations_df[locations_df['Population'].isnull()]
    if not nan_population.empty:
        print(f"Rows with NaN in Population column:\n{nan_population}")

    # Drop rows with NaN values in key columns
    locations_df.dropna(subset=['Latitude', 'Longitude', 'Population'], inplace=True)

    # Prepare data for HeatMap layer
    heat_data = [(row['Latitude'], row['Longitude'], row['Population']) for index, row in locations_df.iterrows()]
    return heat_data


def preprocess_locations_data_for_opt(heat_data):
    """
    Preparing data to be used for optimisation, by dropping population from heat_data

    Parameters:
    Heat_data (list): contains latitudes, longitudes and populations.

    Return:
    opt_data (array): An array of coordinates (town_coordinates) represented as (latitude, longitude)
    """
    opt_data = [(lat, lon) for lat, lon, _ in heat_data]
    return opt_data


def load_devon_boundary(url):
    """
    Load the GeoJSON data for Devon boundary.
    Parameters:
    url (str): URL of the GeoJSON data.
    Returns:
    geopandas.GeoDataFrame: GeoDataFrame containing the Devon boundary data.
    """
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content
        return gpd.read_file(BytesIO(data))
    else:
        return None


def optimize_geodataframe(gdf, column_name, filter_value):
    """
    Optimize a GeoDataFrame based on a filter.
    Parameters:
    gdf (geopandas.GeoDataFrame): The GeoDataFrame to optimize.
    column_name (str): The column name to filter on.
    filter_value (str): The value to filter the column on.
    Returns:
    geopandas.GeoDataFrame: The optimized GeoDataFrame.
    """
    optimized_gdf = gdf[gdf[column_name] == filter_value].copy()
    optimized_gdf.loc[:, 'geometry'] = optimized_gdf['geometry'].simplify(tolerance=0.001)
    return optimized_gdf


def get_graph(lat, lon, dist, filename):
    """
    Load or fetch a graph from a file or by querying OSMnx.
    """
    # Define the cache directory path relative to the main script
    main_script_dir = os.path.dirname(sys.argv[0])
    cache_dir = os.path.join(main_script_dir, 'map_cache')
    os.makedirs(cache_dir, exist_ok=True)

    # Modify the filename to include the cache directory path
    cache_file_path = os.path.join(cache_dir, filename)

    if Path(cache_file_path).is_file():
        with open(cache_file_path, 'rb') as file:
            graph = pickle.load(file)
    else:

        graph = ox.graph_from_point((lat, lon), dist=dist, network_type='drive', simplify=True)
        with open(cache_file_path, 'wb') as file:
            pickle.dump(graph, file)
    return graph


def create_devon_boundary_layer(f_map, devon_gdf):
    """
    Create a Folium FeatureGroup for Devon boundary from a GeoDataFrame.
    """
    devon_boundary_layer = folium.FeatureGroup(name='UK County Boundaries')
    for _, row in devon_gdf.iterrows():
        sim_geo = gpd.GeoSeries(row['geometry']).simplify(tolerance=0.001)
        geo_j = sim_geo.to_json()
        geo_j = folium.GeoJson(data=geo_j,
                               style_function=lambda x: {'fillColor': 'transparent', 'color': 'yellow', 'weight': 4})
        geo_j.add_to(devon_boundary_layer)
    devon_boundary_layer.add_to(f_map)
    return devon_boundary_layer


def get_devon_boundary_polygon(devon_gdf):
    """
    Retrieve the Devon boundary polygon from a GeoDataFrame.
    """
    return devon_gdf.iloc[0]['geometry']


def read_and_combine_geojson(file_urls):
    """
    Read Geojson files from a list of urls and combine them.

    Parameters:
    file_urls (list): List of Geojson file urls.

    Return:
    gdf_chloro_map_data: comined geodataframe

    """
    dfs = []
    for url in file_urls:
        response = requests.get(url)
        geojson_data = response.json()  # Assumes GeoJSON content
        gdf = gpd.read_file(BytesIO(response.content))
        dfs.append(gdf)

    gdf_chloro_map_data = gpd.GeoDataFrame(pd.concat(dfs, ignore_index=True))
    return gdf_chloro_map_data
