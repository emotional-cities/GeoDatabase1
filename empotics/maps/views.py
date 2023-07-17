from django.shortcuts import render,redirect
import requests
import json
import pandas as pd
import geopandas as gpd
import folium
import mysql.connector
from folium import plugins
from folium import Map, FeatureGroup, Marker, LayerControl
from branca.element import MacroElement
from jinja2 import Template
import branca.colormap as cm
import branca

class BindColormap(MacroElement):
    def __init__(self, layer, colormap):
        super(BindColormap, self).__init__()
        self.layer = layer
        self.colormap = colormap
        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            {{this.colormap.get_name()}}.svg[0][0].style.display = 'block';
            {{this._parent.get_name()}}.on('layeradd', function (eventLayer) {
                if (eventLayer.layer == {{this.layer.get_name()}}) {
                    {{this.colormap.get_name()}}.svg[0][0].style.display = 'block';
                }});
            {{this._parent.get_name()}}.on('layerremove', function (eventLayer) {
                if (eventLayer.layer == {{this.layer.get_name()}}) {
                    {{this.colormap.get_name()}}.svg[0][0].style.display = 'none';
                }});
        {% endmacro %}
        """)    

def get_responses(*args):
    """
    Fetches responses from an API for a list of parameters.

    Args:
        *args: Variable number of parameters.

    Returns:
        dict: A dictionary containing the API responses for each parameter.

    Raises:
        None
    """
    
    list_of_responses = {}
    for parm in args:
        print(parm)
        url = f"https://emotional.byteroad.net/collections/{parm}/items?f=json&lang=en-US&limit=10000&skipGeometry=false&offset=0"
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            data_dict = json.loads(response.content)
            list_of_responses[parm] = data_dict
        else:
            print(f'The not working param is {parm}')
            print("Error: API request unsuccessful.")
    return list_of_responses

def connect_to_db():
    """
    Connects to a MySQL database.

    Args:
        None

    Returns:
        mysql.connector.connection.MySQLConnection: A connection object representing the database connection.

    Raises:
        None
    """
    db=mysql.connector.connect(
        host='climateflux.com',
        user='emocities_dash',
        passwd='emocities@CLIMA',
        database='emocities'
    )
    mycursour=db.cursor()
    return db

def get_row(layer,row_name):
    """
    Retrieves a specific row from the database.

    Args:
        layer (str): The layer name.
        row_name (str): The name of the row to retrieve.

    Returns:
        str: The value of the requested row.

    Raises:
        None
    """
    db=connect_to_db()
    mycursor=db.cursor()
    query=f"select {row_name} from metadata_emotics where LayerName = '{layer}'"
    mycursor.execute(query)
    rows=mycursor.fetchall()
    result1=[list(row) for row in rows]
    result=result1[0][0]

    return result

def get_list_nums(layer,row_name):
    """
    Retrieves a list of numbers from a specific row in the database.

    Args:
        layer (str): The layer name.
        row_name (str): The name of the row to retrieve.

    Returns:
        list: A list of numbers extracted from the row.

    Raises:
        None
    """
    row=get_row(layer=layer,row_name=row_name)
    cleaned_row = row.replace('[', '').replace(']', '').replace('\'', '')
    elements = cleaned_row.split(',')
    numbers=[float(element)for element in elements]
    last=numbers.pop()
    las2=numbers.pop()
    return numbers

def get_list_strings(layer,row_name):
    """
    Retrieves a list of strings from a specific row in the database.

    Args:
        layer (str): The layer name.
        row_name (str): The name of the row to retrieve.

    Returns:
        list: A list of strings extracted from the row.

    Raises:
        None
    """
    row=get_row(layer=layer,row_name=row_name)
    cleaned_row = row.replace('[', '').replace(']', '').replace('\'', '')
    elements = cleaned_row.split(',')
    return [element.strip() for element in elements]

def get_layers(city):
    """
    Retrieves a list of layers associated with a specific city.

    Args:
        city (str): The name of the city.

    Returns:
        list: A list of layer names associated with the city.

    Raises:
        None
    """
    db=connect_to_db()
    query=f"select Layername from metadata_emotics where City = '{city}' "
    df=pd.read_sql(query,db)
    layers=df['Layername'].to_list()
    return layers

def get_captions(city):
    """
    Retrieves a list of captions associated with a specific city.

    Args:
        city (str): The name of the city.

    Returns:
        list: A list of captions associated with the city.

    Raises:
        None
    """
    db=connect_to_db()
    query=f"select Caption from metadata_emotics where City = '{city}' "
    df=pd.read_sql(query,db)
    captions=df['Caption'].to_list()
    return captions

def create_map(params,long,lat): #should automize getting the long and the lat
    """
    Creates a folium map with multiple layers based on the given parameters.

    Args:
        params (tuple): Tuple of parameters.
        long (float): Longitude coordinate.
        lat (float): Latitude coordinate.

    Returns:
        folium.Map: Folium map object with multiple layers.

    Raises:
        None
    """
    response_dict = get_responses(*params)
    feature_groups = []
    values=['_mean','wprev_mean','PROB_4BAND','av_age_bui', 'buil_repai', 'av_buil_he', 'buil_area_', 'walkabilit', 'altimetry', 'beds_tour_', 'ff_out_den', 'ndvi', 'gre_spa_po', 'noise', 'pm25', 'pm10', 'mean_temp', 'ex_heat_vu','ffloods_vu','pur_power', 'ppo_low_ed', 'ppop_unemp', 'pop_densit', 'gender_rat', 'yt_peop_ra', 'ed_peop_ra']
    m = folium.Map(location=[long, lat], zoom_start=12, tiles=None) #need to replace the long and lat and make it automated
    base_map = folium.FeatureGroup(name='Basemap', overlay=True, control=False)
    folium.TileLayer(tiles='Stamen Terrain').add_to(base_map)
    base_map.add_to(m)
    for key, response in response_dict.items():
        
        geojson_data = response['features']
        caption=get_row(key,'Caption')
        fg = folium.FeatureGroup(name=caption, overlay=False)
        Thresholds=get_list_nums(key,'Thresholds')
        Colors=get_list_strings(key,'Colors')
        indexes=sorted(list(set(Thresholds)))
        #style=get_style_2(key,Thresholds,Colors)
        i=0
        for feature in geojson_data:
            properties = feature['properties']
            for value in values:
                if value in properties:
                    if i==0:
                        style=get_style_2(key,Thresholds,Colors,value)
                        i=i+1
                    geoj=folium.GeoJson(feature,style_function=style)
                    folium.features.GeoJsonPopup(fields=[value],aliases=['Mean Value'],labels=True,localize=True).add_to(geoj)
                    fg.add_child(geoj)
        scale=branca.colormap.StepColormap(Colors[1:],indexes,vmin=min(indexes),vmax=max(indexes),caption=caption)
                                            
        feature_groups.append(fg)
        m.add_child(fg)
        m.add_child(scale)
        m.add_child(BindColormap(fg,scale))
    
    m.add_child(folium.map.LayerControl('bottomleft', collapsed=False))
    return m


def color_layer(x, thresholds, colors,property):
    """
    Determines the color of a layer based on the value of a specific property.

    Args:
        x (dict): GeoJSON feature dictionary.
        thresholds (list): List of thresholds for color classification.
        colors (list): List of colors corresponding to each threshold.
        property (str): Name of the property used for classification.

    Returns:
        str: Color code for the given feature.

    Raises:
        None
    """
    for i in range(len(colors)-1):
        if i == 0 and x['properties'][property] is not None:
            if x['properties'][property] <= thresholds[i]:  
                return colors[i]
        elif x['properties'][property] is not None:
            if thresholds[(2*i)-1] <= x['properties'][property] < thresholds[(2*i)]:
                return colors[i]
    return colors[-1]


def get_style_2(key,thresholds,colors,property):
    """
    Returns a style function for a GeoJSON layer.

    Args:
        key (str): Key identifier for the layer.
        thresholds (list): List of thresholds for color classification.
        colors (list): List of colors corresponding to each threshold.
        property (str): Name of the property used for classification.

    Returns:
        function: Style function for the GeoJSON layer.

    Raises:
        None
    """
    return lambda x:{'fillColor':color_layer(x,thresholds=thresholds,colors=colors,property=property),'color':'white', 'weight':1, 'fillOpacity': '0.7'}
    

# Example usage
"""
params = ['hex350_grid_ndvi2022', 'hex350_grid_pm25_2019']
create_map(params)
"""
# Create your views here.

def landing_page(request):
    return render(request,'landing_page.html')

def london_page(request):
    layers=get_layers('London')
    captions=get_captions('London')
    meta=zip(layers,captions)
    context={'meta':meta}
    return render(request,'london_page.html',context)

def lansing_page(request):
    return render(request,'lansing_page.html')

def lisbon_page(request):
    layers=get_layers('Lisbon')
    caption=get_captions('Lisbon')
    meta=zip(layers,caption)
    context={'meta':meta}
    return render(request,'lisbon_page.html',context)

def copenhagen_page(request):
    return render(request,'copenhagen_page.html')

def checkbox_page(request):
    if request.method == 'GET':
        selected_options = request.GET.getlist('options')
        print('referal',request.META['HTTP_REFERER'])
        if str(request.META['HTTP_REFERER'])=='http://127.0.0.1:8000/london/':

            map=create_map(selected_options,51.502264, -0.062134)
            map=map._repr_html_()
            context={'map':map}
            return render(request, 'map.html',context)
        elif str(request.META['HTTP_REFERER'])=='http://127.0.0.1:8000/lisbon/':
            map=create_map(selected_options,38.736946, -9.142685)
            map=map._repr_html_()
            context={'map':map}
            return render(request,'map.html',context)
