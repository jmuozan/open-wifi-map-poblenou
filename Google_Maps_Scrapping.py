import requests
from bs4 import BeautifulSoup
import urllib.request

def scrape_google_maps_list(url):
    # Send a GET request to the Google Maps list URL
    response = requests.get(url)
    
    # Parse the HTML content of the response
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all the place cards in the list
    place_cards = soup.find_all('div', class_='suEOdc')
    
    # Print the number of place cards found for debugging
    print("Number of place cards found:", len(place_cards))

    for card in place_cards:
        # Extract metadata
        title_element = card.find('div', class_='cXedhc')
        if title_element:
            title = title_element.text.strip()
            print("Title:", title)
        
        # Extract image URL if available
        image_div = card.find('img')
        if image_div:
            image_url = image_div['./IMG']
            # Save the image
            image_name = f"{title.replace(' ', '_')}.jpg"
            urllib.request.urlretrieve(image_url, image_name)
            print(f"Image saved: {image_name}")
        
        print()

# Example usage
google_maps_list_url = "https://maps.app.goo.gl/1ybVg9QNuHaBypAR7"
scrape_google_maps_list(google_maps_list_url)
