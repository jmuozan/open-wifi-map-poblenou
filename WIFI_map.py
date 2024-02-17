import folium
import pandas as pd

# Import CSV file
data = pd.read_csv('Data.csv')

# Creating map
m = folium.Map(location=[41.399076582716276, 2.198679827227125], zoom_start=16)

# Iterate over each row in the CSV file
for index, row in data.iterrows():
    # CSV location 
    location = [row['Latitude'], row['Longitude']]
    
    # CSV metadata
    popup_content = f"<h1>{row['Place']}</h1>"
    popup_content += f"<div id='slideshow'><img src='{row['Image1']}' height='200px'><img src='{row['Image2']}' height='200px'></div>"
    popup_content += f"<h3>  Wifi around the area {row['WIFIS']} Opened ones {row['Opened']}. You can visit the site <a href='{row['Map_link']}'>here👈</a></h3>"
    
    color = "red"
    if int(row['Opened']) > 0:  # Convertir a número antes de comparar
        color = "green"
    
    # Creating markers
    folium.Circle(
        location=location,
        radius=row['WIFIS'] * 5,
        popup=folium.Popup(popup_content, max_width=800),
        fill=True,
        fill_color=color,
        color=color,
    ).add_to(m)

# Output map
m.save("poblenou.html")
