from geopy.distance import geodesic


def calculate_total_distance(point_coordinates, nodes, coords):
    """
    Calculate the total distance of all point_coordinates to nearest node or new_point.

     Parameters:
    point_coordinates (array): An array of coordinates (town_coordinates) represented as (latitude, longitude).
    nodes (array): An array of nodes (ambulance hubs), each represented as (latitude, longitude).
    coords (array): An array of (latitude, longitude)

    Returns:
    float: Total distance from all point_cordinates (towns) to their nearest node (ambulance hub)
    """
    distances = []
    tuple_coords = tuple(coords)

    for p in point_coordinates:
        distance_amb_hub = []

        for node in nodes + [tuple_coords]:
            d = geodesic((p[0], p[1]), (node[0], node[1])).kilometers
            distance_amb_hub.append(d)

        min_distance = min(distance_amb_hub)
        distances.append(min_distance)

    return sum(distances)
