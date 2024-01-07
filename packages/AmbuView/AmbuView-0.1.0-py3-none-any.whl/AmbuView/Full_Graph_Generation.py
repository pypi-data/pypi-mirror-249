import folium
import time
from AmbuView import data_processing, isochrone_map, map_visualization, optimization
import sys
import os


def create_ambulance_coverage_map(locations_csv=None,
                                  uk_county_boundary_url=None,
                                  pop_density_urls=None,
                                  pop_density_csv=None,
                                  ambulance_hub_lat_lon_tuples=None,
                                  ambulance_time=None):
    script_dir = os.path.dirname(sys.argv[0])
    if locations_csv is None:
        locations_csv = 'Devon 2021 Census Population by town.csv'
    if uk_county_boundary_url is None:
        uk_county_boundary_url = "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/Counties_"\
                                 + "May_2023_Boundaries_EN_BFC/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"
    if pop_density_urls is None:
        pop_density_urls = [
            "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/"
            + "json/statistical/eng/msoa_by_lad/E07000046.json",
            "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/"
            + "json/statistical/eng/msoa_by_lad/E07000040.json",
            "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/"
            + "json/statistical/eng/msoa_by_lad/E07000041.json",
            "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/"
            + "json/statistical/eng/msoa_by_lad/E07000042.json",
            "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/"
            + "json/statistical/eng/msoa_by_lad/E07000043.json",
            "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/"
            + "json/statistical/eng/msoa_by_lad/E07000044.json",
            "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/"
            + "json/statistical/eng/msoa_by_lad/E07000045.json",
            "https://raw.githubusercontent.com/martinjc/UK-GeoJSON/master/"
            + "json/statistical/eng/msoa_by_lad/E07000047.json"]
    if pop_density_csv is None:
        pop_density_csv = "nomis_2023_12_31_000343.csv"
    if ambulance_hub_lat_lon_tuples is None:
        ambulance_hub_lat_lon_tuples = [(50.7169, -3.5064), (50.8100, -4.3540), (51.0167, -4.2089),
                                        (50.7384, -4.0041), (50.7909, -3.6513), (51.0805, -4.0580),
                                        (51.2093, -4.1239), (51.0185, -3.8356), (50.9025, -3.4885),
                                        (50.8555, -3.3925), (50.6190, -3.4139), (50.6805, -3.2395),
                                        (50.7990, -3.1879), (50.7792, -2.9977), (50.4183, -4.1108),
                                        (50.5474, -4.1443), (50.5155, -3.7537), (50.4309, -3.6848),
                                        (50.2838, -3.7766), (50.3525, -3.5797), (50.3948, -3.5159),
                                        (50.4385, -3.5695), (50.4619, -3.5253), (50.5305, -3.6081),
                                        (50.5809, -3.4644), (50.8266, -4.5432), (50.6353, -4.3662),
                                        (51.2052, -3.4776)]
    if ambulance_time is None:
        ambulance_time = 15
    locations_csv_path = os.path.join(script_dir, locations_csv)
    pop_density_csv_path = os.path.join(script_dir, pop_density_csv)

    # Start the timer
    start_time = time.time()

    print('Downloading URL Data')
    locations_df = data_processing.load_locations_from_csv(locations_csv_path)
    post_processed_data = data_processing.preprocess_locations_data(locations_df)
    opt_data = data_processing.preprocess_locations_data_for_opt(post_processed_data)
    devon = data_processing.load_devon_boundary(uk_county_boundary_url)
    data_processing.optimize_geodataframe(devon, 'CTY23NM', 'Devon')
    shapefile_gdf = data_processing.read_and_combine_geojson(pop_density_urls)
    pop_density_df = data_processing.load_locations_from_csv(pop_density_csv_path)

    # Initialize the map with an arbitrary center point and zoom level
    combined_map = folium.Map(location=[50.7169, -3.5064], zoom_start=10)

    # Create Devon boundary layer and add to the map
    data_processing.create_devon_boundary_layer(combined_map, devon)

    # List of ambulance hubs
    ambulance_hubs = ambulance_hub_lat_lon_tuples

    isochrone_layer = folium.FeatureGroup(name='Isochrones')
    isochrone_map.create_isochrones(ambulance_hubs, isochrone_layer, ambulance_time)  # Utilize parallel processing

    map_visualization.add_chloropleth_layer(combined_map, shapefile_gdf, pop_density_df)

    isochrone_layer.add_to(combined_map)

    map_visualization.add_heatmap_layer(combined_map, post_processed_data, 'Population Heatmap')

    map_visualization.add_ambulance_hub_markers(combined_map, ambulance_hubs)

    # Get Devon's boundary polygon
    data_processing.get_devon_boundary_polygon(devon)

    # Add marker for the furthest point within the convex hull
    optimization.add_marker_for_furthest_point(combined_map, ambulance_hubs, opt_data)

    map_visualization.add_layer_control(combined_map)
    print('the total isochrones generated: ' + str(isochrone_map.global_isochrone_count))

    isochrone_map.add_isochrone_legend(combined_map, ambulance_time)

    # Save the combined map to an HTML file
    combined_map.save('combined_isochrone_map.html')

    # End the timer
    end_time = time.time()

    # Calculate total runtime
    total_runtime = end_time - start_time

    print(f"Total Runtime: {total_runtime} seconds")
    print('The map can be found as an HTML file located in the same directory as where you ran the python script named:'
          'combined_isochrone_map.HTML')
