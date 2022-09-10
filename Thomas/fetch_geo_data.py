# find geo data from address

import folium
import requests
import re
import csv, json, xml
import pandas as pd

from pyodide.http import open_url, pyfetch
import asyncio

from collections import namedtuple
import numpy as np
import math

from datetime import datetime

async def get_geo(e): 
    # set and get infos parking garage from csv file

    url_content = open_url("https://service-datenbank.de/parking_garage_infos.csv")
    dfPG = pd.read_csv(url_content)
    dfPG = dfPG.drop('lat', axis=1)
    dfPG = dfPG.drop('lng', axis=1)
    dfPG.fillna("", inplace = True)   
    dfPG.loc[dfPG['longname'].str.strip() == '', 'longname'] = dfPG['title']
    #pyscript.write('output',dfPG['status'].dtypes)
    # add color to dataframe
    dfPG.loc[(dfPG['free'] >= 100) & (dfPG['status'] == 1), 'color'] = 'darkgreen'
    dfPG.loc[(dfPG['free'] < 100) & (41 < dfPG['free']) & (dfPG['status'] == 1), 'color'] = 'green'
    dfPG.loc[(dfPG['free'] <= 41) & (1 < dfPG['free']) & (dfPG['status'] == 1), 'color'] = 'lightgreen'
    dfPG.loc[(dfPG['free'] < 1), 'color'] = 'red'
    dfPG.loc[(dfPG['status'] < 0), 'color'] = 'red'
    #pyscript.write('output',dfPG.head())
    
    # colors Markers
    # 'red',
    # 'blue',
    # 'gray',
    # 'darkred',
    # 'lightred',
    # 'orange',
    # 'beige',
    # 'green',
    # 'darkgreen',
    # 'lightgreen',
    # 'darkblue',
    # 'lightblue',
    # 'purple',
    # 'darkpurple',
    # 'pink',
    # 'cadetblue',
    # 'lightgray',
    # 'black'
    
    gewaehlteFilterCS = Element('gewaehlteFilterCS').value
    #print(gewaehlteFilterCS)
    gewaehlteFilterPS = Element('gewaehlteFilterPS').value
    #print(gewaehlteFilterPS) 
    gewaehlteFilterPG = Element('gewaehlteFilterPG').value
    #print(gewaehlteFilterPG)
    gewaehlteFilterPR = Element('gewaehlteFilterPR').value
    #print(gewaehlteFilterPR)
    gewaehlteFilterPM = Element('gewaehlteFilterPM').value
    #print(gewaehlteFilterPM)
    address = Element('zielort').value
    #print(address)
    response = await pyfetch(url='https://nominatim.openstreetmap.org/search?format=json&q=' + address, method="GET")
    output1 = await response.json()
    # it is possible you get more than one findings
    output1 = str(output1[0])    
    #print(output1)
    # bring the output in normal json format
    output2 = output1.replace("'","\"").replace("[{","{").replace("}]","}")
    #print(output2)
    
    # parse output from json:
    output3 = json.loads(output2)
    #print(output3)
    #tag = []
    #for tag in output3:
    #    print (tag)
        
    # find latitude from output:
    target_lat = output3["lat"]
    #print(target_lat)

    # find lon from output:
    target_lon = output3["lon"]
    #print(target_lon)
    #'lat': '50.922625', 'lon': '6.935974015806089'

    #pyscript.write('request_output', output)
    #output4 =  f"Get GEO Data Target: {address} lat: {target_lat} lon: {target_lon} checked: {gewaehlteFilterPSt} | {gewaehlteFilterPS} | {gewaehlteFilterPG} | {gewaehlteFilterPR} | {gewaehlteFilterPM}"
    output4 =  f"Get GEO Data Target: {address} lat: {target_lat} lon: {target_lon}"
 
    pyscript.write('outputGEODATATARGET', output4)
  
    addressStart = Element('startort').value
    #print(addressStart)
    response = await pyfetch(url='https://nominatim.openstreetmap.org/search?format=json&q=' + addressStart, method="GET")
    output1 = await response.json()
    # it is possible you get more than one findings
    output1 = str(output1[0])    
    #print(output1)
    # bring the output in normal json format
    output2 = output1.replace("'","\"").replace("[{","{").replace("}]","}")
    #print(output2)
    
    # parse output from json:
    output3 = json.loads(output2)
    #print(output3)
    #tag = []
    #for tag in output3:
    #    print (tag)
        
    # find latitude from output:
    start_lat = output3["lat"]
    #print(start_lat)
    
    # find lon from output:
    start_lon = output3["lon"]
    #print(start_lon)
    #'lat': '50.922625', 'lon': '6.935974015806089'
    #pyscript.write('request_output', output) 
    output4 =  f"Get GEO Data Start: {addressStart} lat: {start_lat} lon: {start_lon}"
    pyscript.write('outputGEODATASTART', output4)
    
    # only card
    pyscript.write('foliummap', '')
    m = folium.Map(location=[target_lat, target_lon], zoom_start=15) #, width=800, height=400)
    folium.LayerControl().add_to(m)
 
    # set and get marker from csv file

    url_content = open_url("https://service-datenbank.de/merged_data.csv")
    
    df = pd.read_csv(url_content, sep = ",", na_values = "MISSING_DATA")
    df.fillna("-", inplace = True)
    #pyscript.write('output',df.head())
    #print('output',df.columns)
    #pyscript.write('output',df.info())
    
    # merge the two dataframes df and dfPG
    
    #df = pd.merge(df, dfPG, how ='inner', on ='identifier') 
    #df = pd.concat([df, dfPG], axis = 1)
    df = pd.merge(df, dfPG, how="left", on="identifier") 
    

    # Pick only those rows where in near starts with "50....".

    df["y"] = df["y"].astype(str)
    #print('output',df.info())
    df = df[df["y"].str.startswith(target_lat[0:5])]
    #print(target_lat[0:5])
    #pyscript.write('output',df)
    df["y"] = df["y"].astype(float)
    #print(df.info())

    # Pick only those rows where in near starts with "6....".

    df["x"] = df["x"].astype(str)
    #print('output',df.info())
    df = df[df["x"].str.startswith(target_lon[0:4])]
    #print(target_lon[0:4])
    #pyscript.write('output',df)
    df["x"] = df["x"].astype(float)
    #print(df.info())

    # change df["kapazitaet, stellplaetze, Stellplätze"] into int
    # Replace SubString using apply() function with lambda.
    #df = df.apply(lambda x: x.replace({'Py':'Python with', 'Language':'Lang'}, regex=True))
    # Replace multiple substrings
    df["kapazitaet"] = df["kapazitaet"].astype(str)
    df["stellplaetze"] = df["stellplaetze"].astype(str)
    df["Stellplätze"] = df["Stellplätze"].astype(str)
    df["free"] = df["free"].astype(str)
    df["open_time"] = df["open_time"].astype(str)
    df["close_time"] = df["close_time"].astype(str)
    df["timestamp"] = df["timestamp"].astype(str)
    #df["tendenz"] = df["tendenz"].astype(str)
    df["longname"] = df["longname"].astype(str)
    df["title"] = df["title"].astype(str)
    #df["slug"] = df["slug"].astype(str)
    df["street"] = df["street"].astype(str)
    df["housenumber"] = df["housenumber"].astype(str)
    df["womens_parking"] = df["womens_parking"].astype(str)
    df["price"] = df["price"].astype(str)
    df["phone"] = df["phone"].astype(str)	
    df["open"] = df["open"].astype(str)
    df["extra_info"] = df["extra_info"].astype(str)
    df["entry_height"] = df["entry_height"].astype(str)
    df["entry_width"] = df["entry_width"].astype(str)
    df["capacity_brutto"] = df["capacity_brutto"].astype(str)
    #df["volltext"] = df["volltext"].astype(str)
    df["notice"] = df["notice"].astype(str) 

    
    df = df.replace({'stellplaetze': '.0','Stellplätze': '.0','HPD/Std.': '.0' ,'kapazitaet': '.0','Anzahl Ladepunkte': '.0','free': '.0','housenumber': '.0', 'entry_height': '1.','entry_width': '2.'}, 
    {'stellplaetze': '','Stellplätze': '','HPD/Std.': '','kapazitaet': '','Anzahl Ladepunkte': '','free': '','housenumber': '','entry_height': '1,','entry_width': '2,'}, regex=True)
     
    df = df.replace(['-'],'')
    df = df.replace(['nan'],'')
    #print(df) 

    # Get names of indexes for drop
    if (gewaehlteFilterCS == 'Charging Station NOT checked'):
    
        indexFilterDrop = df[ (df['type'] == 'charging station') ].index
        # Delete these row indexes from dataFrame
        df.drop(indexFilterDrop , inplace=True)
    
    if (gewaehlteFilterPS == 'Parking Slot NOT checked'):
    
        indexFilterDrop = df[ (df['type'] == 'disabled parking slot') ].index
        # Delete these row indexes from dataFrame
        df.drop(indexFilterDrop , inplace=True)

    if (gewaehlteFilterPG == 'Park Garage NOT checked'):
    
        indexFilterDrop = df[ (df['type'] == 'parking garage') ].index
        # Delete these row indexes from dataFrame
        df.drop(indexFilterDrop , inplace=True)
        
    if (gewaehlteFilterPR == 'Park and Ride NOT checked'):
    
        indexFilterDrop = df[ (df['type'] == 'park and ride') ].index
        # Delete these row indexes from dataFrame
        df.drop(indexFilterDrop , inplace=True)
    
    if (gewaehlteFilterPM == 'Park Meter NOT checked'):
    
        indexFilterDrop = df[ (df['type'] == 'parking meter') ].index
        # Delete these row indexes from dataFrame
        df.drop(indexFilterDrop , inplace=True)

    #print(df)
    
    # find the right columns for parking situation
  
    #df["name"] = np.where(df["type"] == "disabled parking slot", "ID: " + " " + df["key_id"].map(str) + "<br></br> Type: parking slot <br></br> Adresse: " + df["bezeichnung"].map(str) + " " + df["stadtteil"].map(str) + "<br></br> Geo: " + df["x"].map(str) + " " + df["y"].map(str), \
    #(np.where(df["type"] == "parking garage", "ID: " + " " + df["key_id"].map(str) + "<br></br> Type: parking garage " + " <br></br> Identifier: " + df["identifier"] + "<br></br> Parkhaus: " + df["parkhaus"] + " " + df["name"]  + "<br></br> Adresse: " + df["street"].map(str) + " " + df["housenumber"].map(str) + "<br></br> Kapazität: " + df["kapazitaet"] + " Kapazität:? " + df["capacity_brutto"].map(str)  + "<br></br> Frei: " + df["free"].map(str) + "<br></br> Öffnungszeiten: " + df["open_time"].map(str) + " Schliesszeiten: " + df["close_time"].map(str) + "<br></br> Aktualisierung: " + df["timestamp"].map(str) + "<br> Frauenparkplätze: " + df["womens_parking"].map(str) + "<br> Preis: " + df["price"].map(str) + "<br> Offen: " + df["open"].map(str) + "<br> Infos: " + df["extra_info"].map(str) + "<br> Einfahrtshöhe: " + df["entry_height"].map(str) + "<br> Einfahrtsbreite: " + df["entry_width"].map(str) + "<br></br> Telefon: " + df["phone"].map(str)  + "<br> Notizen: " + df["notice"].map(str) + "<br></br> Geo: " + df["x"].map(str) + " " + df["y"].map(str), \
    #(np.where(df["type"] == "parking meter", "ID: " + " " + df["key_id"].map(str) + "<br></br> Type: parking meter " + "<br></br> Aufstellort: " + df["Aufstellort"].map(str)	+ "<br></br> Bezirk/Gebiet: " + df["Bezirk/Gebiet"].map(str)	+ "<br></br> Abschnitt/-von: " + df["Abschnitt/-von"].map(str)	+ "<br></br> Abschnitt/-bis: " + df["Abschnitt/-bis"].map(str)	+ "<br></br> Stellplätze: " + df["Stellplätze"].map(str)	+ "<br></br> Gebührenzeit: " + df["Gebuehrenzeit"].map(str)	+ "<br></br> Gebühr je 15 Minuten: " + df["Gebuehr je 15 Minuten"].map(str)	+ "<br></br> HPD/Std.: " + df["HPD/Std."].map(str)	+ "<br></br> Tagesgebuehr: " + df["Tagesgebuehr"].map(str) + "<br></br> Geo: " + df["x"].map(str) + " " + df["y"].map(str), \
    #(np.where(df["type"] == "charging station", "ID: " + " " + df["key_id"].map(str) + "<br></br> Type: charging station " + " " + df["Straße"].map(str)	+ " " + df["Hausnummer"].map(str)	+ " " + df["Adresszusatz"].map(str)	+ "<br></br>  Inbetriebnahmedatum: " + df["Inbetriebnahmedatum"].map(str)	+ "<br></br> Anschlussleistung: " + df["Anschlussleistung"].map(str)	+ "<br></br>  Art der Ladeeinrichung: " + df["Art der Ladeeinrichung"].map(str)	+ "<br></br>  Anzahl Ladepunkte: " + df["Anzahl Ladepunkte"].map(str)	+ "<br></br> Steckertypen1: " + df["Steckertypen1"].map(str)	+ " P1 [kW]: " + df["P1 [kW]"].map(str)	+ " Public Key1: " + df["Public Key1"].map(str)	+ "<br></br> Steckertypen2: " + df["Steckertypen2"].map(str)	+ " P2 [kW]: " + df["P2 [kW]"].map(str)	+ " Public Key2: " + df["Public Key2"].map(str)	+ "<br></br> Steckertypen3: " + df["Steckertypen3"].map(str)	+ " P3 [kW]: " + df["P3 [kW]"].map(str)	+ " Public Key3: " + df["Public Key3"].map(str)	+ "<br></br> Steckertypen4: " + df["Steckertypen4"].map(str)	+ " P4 [kW]: " + df["P4 [kW]"].map(str)	+ " Public Key4: " + df["Public Key4"].map(str) + "<br></br> Geo: " + df["x"].map(str) + " " + df["y"].map(str), \
    #(np.where(df["type"] == "park and ride", "ID: " + " " + df["key_id"].map(str) + "<br></br> Type: park and ride " + "<br></br>  Standort: " + df["name"].map(str)	+ " " + df["strasse"].map(str)	+ " " + df["plz"].map(str)	+ " " + df["stadt"].map(str)	+ "<br></br> Stellplätze: " + df["stellplaetze"].map(str)	+ "<br></br> Link: " + df["hyperlink"].map(str)	+ "<br></br> Öffnungszeiten: " + df["oeffnungszeiten"].map(str)	+ "<br></br> Verbindungen: " + df["verbindungen"].map(str) + "<br></br> Geo: " + df["x"].map(str) + " " + df["y"].map(str) , "no values")))))))))
    df["name"] = np.where(df["type"] == "disabled parking slot", "<h3><strong>Address:</strong> " + df["bezeichnung"].map(str) + " " + df["stadtteil"].map(str) + "<br> <a href=\"https://www.google.com/maps/dir/"+addressStart+"/"+ df["y"].map(str)+ "+"+df["x"].map(str)  +"\" target=\"_blank\">Visit GoogleMaps</a></h3>", \
    (np.where(df["type"] == "parking garage", "<h3><strong>Parking garage:</strong> " + df["longname"]  + "<br> Address: " + df["street"].map(str) + " " + df["housenumber"].map(str) + "<br> Capacity: " + df["capacity_brutto"].map(str)  + "<br> Free: " + df["free"].map(str) + "<br> Opening hours: " + df["open_time"].map(str) + " Closing times: " + df["close_time"].map(str) + "<br> Update time: " + df["timestamp"].map(str) + "<br> Womens parking: " + df["womens_parking"].map(str) + "<br> Price " + df["price"].map(str) + "<br> Open: " + df["open"].map(str) + "<br> Infos: " + df["extra_info"].map(str) + "<br> Entrance height:" + df["entry_height"].map(str) + "0m<br> Entrance width: " + df["entry_width"].map(str) + "0m<br> Phone: " + df["phone"].map(str)  + "<br> Notes: " + df["notice"].map(str) + "<br> <a href=\"https://www.google.com/maps/dir/"+addressStart+"/"+ df["y"].map(str)+ "+"+df["x"].map(str)  +"\" target=\"_blank\">Visit GoogleMaps</a></h3>", \
    (np.where(df["type"] == "parking meter", "<h3><strong>Location:</strong> " + df["Aufstellort"].map(str)	+ "<br> District/Area: " + df["Bezirk/Gebiet"].map(str)	+ "<br> Section/-of: " + df["Abschnitt/-von"].map(str)	+ "<br> Section/-to: " + df["Abschnitt/-bis"].map(str)	+ "<br> Plots: " + df["Stellplätze"].map(str)	+ "<br> Fee time: " + df["Gebuehrenzeit"].map(str)	+ "<br> Fee per 15 minutes: " + df["Gebuehr je 15 Minuten"].map(str)	+ "<br> HPD/Std.: " + df["HPD/Std."].map(str)	+ "<br> Daily fee: " + df["Tagesgebuehr"].map(str) + "<br> <a href=\"https://www.google.com/maps/dir/"+addressStart+"/"+ df["y"].map(str)+ "+"+df["x"].map(str)  +"\" target=\"_blank\">Visit GoogleMaps</a></h3>", \
    (np.where(df["type"] == "charging station", "<h3><strong>Address:</strong> " + " " + df["Straße"].map(str)	+ " " + df["Hausnummer"].map(str)	+ " " + df["Adresszusatz"].map(str)	+ "<br>  Inbetriebnahmedatum: " + df["Inbetriebnahmedatum"].map(str)	+ "<br> Anschlussleistung: " + df["Anschlussleistung"].map(str)	+ "<br>  Type of charging equipment: " + df["Art der Ladeeinrichung"].map(str)	+ "<br>  Number of charging points: " + df["Anzahl Ladepunkte"].map(str)	+ "<br> Connector types 1: " + df["Steckertypen1"].map(str)	+ " P1 [kW]: " + df["P1 [kW]"].map(str)	+ " Public Key1: " + df["Public Key1"].map(str)	+ "<br> Connector types 2: " + df["Steckertypen2"].map(str)	+ " P2 [kW]: " + df["P2 [kW]"].map(str)	+ " Public Key2: " + df["Public Key2"].map(str)	+ "<br> Connector types 3: " + df["Steckertypen3"].map(str)	+ " P3 [kW]: " + df["P3 [kW]"].map(str)	+ " Public Key3: " + df["Public Key3"].map(str)	+ "<br> Connector types 4: " + df["Steckertypen4"].map(str)	+ " P4 [kW]: " + df["P4 [kW]"].map(str)	+ " Public Key4: " + df["Public Key4"].map(str) + "<br> <a href=\"https://www.google.com/maps/dir/"+addressStart+"/"+ df["y"].map(str)+ "+"+df["x"].map(str)  +"\" target=\"_blank\">Visit GoogleMaps</a></h3>", \
    (np.where(df["type"] == "park and ride", "<h3><strong>Location:</strong> " + df["name"].map(str)	+ " " + df["strasse"].map(str)	+ " " + df["plz"].map(str)	+ " " + df["stadt"].map(str)	+ "<br> Plots: " + df["stellplaetze"].map(str)	+ "<br> Link: " + df["hyperlink"].map(str)	+ "<br> Opening hours: " + df["oeffnungszeiten"].map(str)	+ "<br> Connections: " + df["verbindungen"].map(str) + "<br> <a href=\"https://www.google.com/maps/dir/"+addressStart+"/"+ df["y"].map(str)+ "+"+df["x"].map(str)  +"\" target=\"_blank\">Visit GoogleMaps</a></h3>", "sorry no values")))))))))
    

    # color marker
    df['color'] = np.where(df['type'] == 'disabled parking slot', 'orange', \
    (np.where(df["type"] == "parking garage",df["color"],\
    (np.where(df["type"] == "parking meter",'purple',\
    (np.where(df["type"] == "charging station",'blue','beige')))))))
    
    #print(df)
    #print(name)
    # make a data frame with dots to show on the map

    #df["name"] = df["key_id"].map(str) + " Address: " + df["bezeichnung"].map(str) + " " + df["stadtteil"].map(str) + " " + df["name"].map(str) + " " + df["strasse"].map(str) + " " + df["plz"].map(str) + " " + df["stadt"].map(str) + df["Straße"].map(str) + " " + df["Hausnummer"].map(str) + " " + df["Adresszusatz"].map(str) + " " + df["Postleitzahl"].map(str) + " " + df["Ort"].map(str) + " " + df["oeffnungszeiten"].map(str) + " " + df["verbindungen"].map(str) + " " + df["Aufstellort"].map(str) + " " + df["Bezirk/Gebiet"].map(str) + " " + df["Abschnitt/-von"].map(str) + " " + df["Abschnitt/-bis"].map(str) + " Plots: "  + df["stellplaetze"].map(str)  + " " + df["Stellplätze"].map(str)  + " " + df["kapazitaet"].map(str) + " Opening hours: " + df["Gebuehrenzeit"].map(str) + " Gebühren: " + df["Gebuehr je 15 Minuten"].map(str) + " " + df["HPD/Std."].map(str) + " " + df["Tagesgebuehr"].map(str)  + " " + df["parkhaus"].map(str) + " " + df["tendenz"].map(str) + " " + df["Anschlussleistung"].map(str) + " " + df["Art der Ladeeinrichung"].map(str) + " " + df["Anzahl Ladepunkte"].map(str) + " " + df["Steckertypen1"].map(str) + " " + df["P1 [kW]"].map(str) + " " + df["Public Key1"].map(str) + " " + df["Steckertypen2"].map(str) + " " + df["P2 [kW]"].map(str) + " " + df["Public Key2"].map(str) + " " + df["Steckertypen3"].map(str) + " " + df["P3 [kW]"].map(str) + " " + df["Public Key3"].map(str) + " " + df["Steckertypen4"].map(str) + " " + df["P4 [kW]"].map(str) + " " + df["Public Key4"].map(str)              + " Geo: " + df["x"].map(str) + " " + df["y"].map(str) + " Type: " + df["type"].map(str)

    df = df.rename(columns={"x": "lon", "y": "lat"})

    df = df[["name","lon","lat","color"]]
    #print(df)
        
    #pyscript.write('output',df.info())    

    data = df
    
    # add marker one by one on the map
    for i in range(0,len(data)):
        folium.Marker(
            location=[data.iloc[i]['lat'], data.iloc[i]['lon']],
            popup=folium.Popup(data.iloc[i]['name'], max_width=2650),
            icon=folium.Icon(color=data.iloc[i]['color']),
        ).add_to(m)
    
    # set marker start and target

    folium.Marker(
        name="startort",
        location=[start_lat, start_lon],
        popup=folium.Popup(f"<h3><strong>Start:</strong> {Element('startort').value}</h3>", max_width=2650, max_height=50),
        icon=folium.Icon(color="black"),
    ).add_to(m)
    
    folium.Marker(
        name="zielort",
        location=[target_lat, target_lon],
        popup=folium.Popup(f"<h3><strong>Target:</strong> {Element('zielort').value} <a href=\"https://www.google.com/maps/dir/{Element('startort').value}/{Element('zielort').value}\" target=\"_blank\">Visit GoogleMaps</a></h3>", max_width=2650, max_height=50),
        icon=folium.Icon(color="black"),
    ).add_to(m)
    start_lon = float(start_lon)
    start_lat = float(start_lat)
    target_lon = float(target_lon)
    target_lat = float(target_lat)
    start = [start_lat,start_lon]
    target = [target_lat,target_lon]
    folium.PolyLine(locations=[start, target], color='red').add_to(m)

    # show the map again
    pyscript.write('foliummap', m)
    
    # show all data from parking garage in outputPG

    url_content = open_url("https://service-datenbank.de/parking_garage_infos.csv")
    dfPG1 = pd.read_csv(url_content)
    dfPG1 = dfPG1.drop('lat', axis=1)
    dfPG1 = dfPG1.drop('lng', axis=1)
    dfPG1.fillna("", inplace = True) 
    dfPG1.loc[dfPG1['longname'].str.strip() == '', 'longname'] = dfPG1['title']
    dfPG1 = dfPG1.sort_values(by=['longname'], ignore_index=True)
    
    #pk0 = "Parking garage: " + dfPG1["longname"][0] + " " + dfPG1["street"][0]  + " " + str(dfPG1["housenumber"][0]) + " Freie Parkplätze: " + str(dfPG1["free"][0])
    #pg = str(i) + "Parking garage: " + dfPG1["longname"][i] + " " + dfPG1["street"][i]  + " " + str(dfPG1["housenumber"][i]) + " Freie Parkplätze: " + str(dfPG1["free"][i])
    
    # show last timestamp 
    dfPG100 = dfPG1["timestamp"][0]
    dfPG100 = datetime.strptime(dfPG100, "%Y-%m-%d %H:%M:%S")
    dfPG100 = dfPG100.strftime("%H:%M:%S %d.%m.%Y")
    pg100 = "Last Timestamp: " + str(dfPG100)
    pyscript.write('outputPG100', pg100) 
    
    for i in dfPG1.index:
        if dfPG1['free'][i] >= 100 and dfPG1['status'][i] == 1:
            pg = ' <strong>' + dfPG1['longname'][i] + '</strong> ' + ' a lot of free parking spaces <div style="color:#006400"><strong>' + str(dfPG1['free'][i]) + '</strong><br><div style="color:#000"> Tendency: ' + str(dfPG1['tendenz'][i]).replace('0','<a style="color:#000">stays').replace('-1','<a style="color:#006400">becomes less').replace('1','<a style="color:red">becomes fuller').replace('2','<a style="color:red">becomes fuller')
            outputPG = 'outputPG'
            outputPG = outputPG + str(i)
        elif dfPG1['free'][i] < 100 and 41 < dfPG1['free'][i] and dfPG1['status'][i] == 1:
            pg = ' <strong>' + dfPG1['longname'][i] + '</strong> ' + ' free parking spaces <div style="color:#008000"><strong>' + str(dfPG1['free'][i]) + '</strong><br><div style="color:#000"> Tendency: ' + str(dfPG1['tendenz'][i]).replace('0','<a style="color:#000">stays').replace('-1','<a style="color:#006400">becomes less').replace('1','<a style="color:red">becomes fuller').replace('2','<a style="color:red">becomes fuller')
            outputPG = 'outputPG'
            outputPG = outputPG + str(i)
        elif dfPG1['free'][i] < 41 and 1 < dfPG1['free'][i] and dfPG1['status'][i] == 1:
            pg = ' <strong>' + dfPG1['longname'][i] + '</strong> ' + ' parking spaces are still available <div style="color:#00FF00"><strong>' + str(dfPG1['free'][i]) + '</strong><br><div style="color:#000"> Tendency: ' + str(dfPG1['tendenz'][i]).replace('0','<a style="color:#000">stays').replace('-1','<a style="color:#006400">becomes less').replace('1','<a style="color:red">becomes fuller').replace('2','<a style="color:red">becomes fuller')
            outputPG = 'outputPG'
            outputPG = outputPG + str(i)
        elif dfPG1['status'][i] == 0:
            pg = ' <strong>' + dfPG1['longname'][i] + '</strong> ' + ' parking not available <div style="color:red"><strong>' 
            outputPG = 'outputPG'
            outputPG = outputPG + str(i)
        else:
            pg = ' <strong>' + dfPG1['longname'][i] + '</strong> ' + ' Parking garage full <div style="color:red"><strong>' + str(dfPG1['free'][i]) + '</strong><br><div style="color:#000"> Tendency: ' + str(dfPG1['tendenz'][i]).replace('0','<a style="color:#000">stays').replace('-1','<a style="color:#006400">becomes less').replace('1','<a style="color:red">becomes fuller').replace('2','<a style="color:red">becomes fuller')
            outputPG = 'outputPG'
            outputPG = outputPG + str(i)
        #print(outputPG)
        pyscript.write(outputPG, pg)