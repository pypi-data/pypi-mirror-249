import numpy as np
from shapely import MultiPoint
from scipy.optimize import minimize
from AmbuView import distance_calculations
import folium


def maximize_distance_within_convex_hull(nodes, point_coordinates):
    """
    Find the point within the convex hull of the nodes that is the furthest away from all nodes.

    Parameters:
    nodes (array): An array of nodes, each represented as (latitude, longitude).

    Returns:
    tuple: The point (latitude, longitude) that is the furthest away from all nodes.
    """
    multipoint = MultiPoint(nodes)
    convex_hull_polygon = multipoint.convex_hull

    # Use the centroid of the convex hull as the initial guess
    centroid = np.array(convex_hull_polygon.centroid.coords[0])
    print("centroid location = ", centroid)
    print('Running new hub optimization algorithm...')

    def objective_function(coords):
        return distance_calculations.calculate_total_distance(point_coordinates, nodes, coords)

    # Optimization within the convex hull
    result = minimize(objective_function, centroid,
                      bounds=[(convex_hull_polygon.bounds[0], convex_hull_polygon.bounds[2]),
                              (convex_hull_polygon.bounds[1], convex_hull_polygon.bounds[3])], method='nelder-mead')

    return result.x


def add_marker_for_furthest_point(f_map, nodes, point_coordinates):
    """
    Add a marker for the furthest point within the convex hull of given nodes on the map.

    Parameters:
    map (folium.Map): The map to add the marker to.
    nodes (array): An array of nodes, each represented as (latitude, longitude).
    """
    furthest_point = maximize_distance_within_convex_hull(nodes, point_coordinates)
    folium.Marker(
        furthest_point,
        popup="<b>Furthest Point within Convex Hull from Central Nodes</b>",
        icon=folium.Icon(color="green", icon="flag")
    ).add_to(f_map)
    print(f"The furthest point within the convex hull from all central nodes is at: {furthest_point}")
    return furthest_point
