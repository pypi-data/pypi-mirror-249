import folium
from folium.plugins import HeatMap
from folium.map import LayerControl


# Function to add an ambulance hub marker to the map
def add_ambulance_hub_markers(f_map, ambulance_hubs):
    """
    Add markers for ambulance hubs on the map.

    Parameters:
    map (folium.Map): The map to add the markers to.
    ambulance_hubs (list of tuple): List of tuples containing the latitude and longitude of the hubs.
    """
    for lat, lon in ambulance_hubs:
        folium.Marker(
            [lat, lon],
            popup="<b>Ambulance Hub</b>",
            icon=folium.Icon(color="blue", icon="ambulance", prefix="fa")
        ).add_to(f_map)


def add_heatmap_layer(f_map, data, layer_name='Heatmap'):
    """
    Add a heatmap layer to the map within a FeatureGroup for toggling.
    """
    heatmap_layer = HeatMap(data, min_opacity=0.5, radius=25, blur=15, max_zoom=1)
    feature_group = folium.FeatureGroup(name=layer_name)
    feature_group.add_child(heatmap_layer)
    feature_group.add_to(f_map)


def add_chloropleth_layer(f_map, shapefile_gdf, pop_density_df):
    """
    Add a choropleth layer to the map with a tooltip to show population density on click.
    """
    merged = shapefile_gdf.set_index("MSOA11CD").join(pop_density_df.set_index("Id"))
    merged.columns = merged.columns.str.strip().str.lower().str.replace(' ', '_')
    threshold_scale = [0, 100, 500, 1000, 5000, 10000]

    # Create a choropleth layer
    choropleth = folium.Choropleth(
        geo_data=merged,
        name='Population Density / Square Km',
        data=merged,
        columns=['msoa11nm', 'population'],
        key_on='feature.properties.msoa11nm',
        threshold_scale=threshold_scale,
        fill_opacity=0.5,
        line_opacity=0.5,
        legend_name='Population Density / Square Km',
        fill_color='YlOrRd'
    )

    # Add tooltip
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['msoa11nm', 'population'], labels=True)
    )

    choropleth.add_to(f_map)


def add_layer_control(f_map):
    """
    Add layer control to the map.
    Parameters:
    map (folium.Map): The map to add the layer control to.
    """
    LayerControl().add_to(f_map)
