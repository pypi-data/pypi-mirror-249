import numpy as np
import osmnx as ox
import networkx as nx
import folium
import alphashape
from shapely import MultiPoint
from shapely.geometry import Polygon, MultiPolygon
from concurrent.futures import ThreadPoolExecutor, as_completed
from AmbuView import data_processing

global_isochrone_count = 0


def create_isochrones(ambulance_hubs, isochrone_layer, ambulance_time=15, isotype='concave'):
    print('Processing isochrones...')
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_node, node, isochrone_layer, ambulance_time, isotype) for node in
                   ambulance_hubs]
        for future in as_completed(futures):
            future.result()


def process_node(node, isochrone_layer, ambulance_time=15, isotype='concave'):
    lat, lon = node
    filename = f'graph_{lat}_{lon}.pkl'
    add_isochrone_to_map(isochrone_layer, lat, lon, filename, time_minutes=ambulance_time, isotype=isotype)


def add_isochrone_to_map(f_map, lat, lon, filename, time_minutes, custom_alpha=30, dist=15000, speed_kmph=60,
                         isotype='concave', allow_multipolygon=False):
    global global_isochrone_count

    """
    Add an isochrone polygon to an existing map for a given central point.

    Parameters:
    map (folium.Map): The map to add the isochrone to.
    lat (float): Latitude of the central point.
    lon (float): Longitude of the central point.
    custom_alpha (float): Alpha value for the alpha shape. Set to None for auto-generated.
    dist (int): Distance around the central point to consider (in meters).
    speed_kmph (int): Speed in kilometers per hour.
    time_minutes (int): Time in minutes.
    """
    # Load the graph for the area
    graph = data_processing.get_graph(lat, lon, dist, filename)

    # Calculate max travel distance in meters
    speed_mpm = (speed_kmph * 1000) / 60
    max_travel_distance_m = speed_mpm * time_minutes

    # Find the nearest node to the central point
    center_node = ox.nearest_nodes(graph, lon, lat)

    # Calculate the reachable nodes within the travel distance
    reachable_nodes = nx.single_source_dijkstra_path_length(graph, center_node, weight='length',
                                                            cutoff=max_travel_distance_m)

    # Collect coordinates of terminal nodes
    terminal_coords = [(graph.nodes[node]['y'], graph.nodes[node]['x']) for node, path_length in reachable_nodes.items()
                       if path_length > 0]
    # Calculate shape based on isotype
    if isotype == 'concave':
        alpha_shape = alphashape.alphashape(np.array(terminal_coords), custom_alpha)

        if isinstance(alpha_shape, Polygon):
            alpha_shapes = [alpha_shape]
        elif isinstance(alpha_shape, MultiPolygon) and allow_multipolygon:
            alpha_shapes = list(alpha_shape.geoms)
        else:
            print(f"Skipped adding shape for {lat}, {lon} as it's not a suitable polygon shape.")
            return  # Skip adding this shape

        for shape in alpha_shapes:
            shape_coords = [(point[0], point[1]) for point in shape.exterior.coords]
            folium.Polygon(shape_coords, color='blue', fill=True, fill_color='blue', fill_opacity=0.3).add_to(f_map)
            global_isochrone_count += 1
            print('number of isochrones added: ' + str(global_isochrone_count))

        else:
            return
    elif isotype == 'convex':
        # Calculate the convex hull
        alpha_shape = MultiPoint(terminal_coords).convex_hull
        shape_coords = [(point[0], point[1]) for point in alpha_shape.exterior.coords]
        folium.Polygon(shape_coords, color='red', fill=True, fill_color='red', fill_opacity=0.5).add_to(f_map)


def add_isochrone_legend(f_map, time_minutes):
    """
    Add a custom legend to the map indicating the isochrone time.

    Parameters:
    map (folium.Map): The map to add the legend to.
    time_minutes (int): The time in minutes used for isochrone calculations.
    """
    legend_html = f'''
    <div style="position: fixed; 
                bottom: 50px; left: 50px; width: 150px; height: 90px; 
                border:2px solid grey; z-index:9999; font-size:14px;
                background-color:white; padding:10px;">
        <b> Isochrone Time </b><br>
        {time_minutes} minutes
    </div>
    '''
    f_map.get_root().html.add_child(folium.Element(legend_html))
