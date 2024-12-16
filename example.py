""" example.py """

import time

import requests

API_KEY = 'AIzaSyDcgn19Abl015v_NaOaz6uCC6c3c9VIbHk'
#type = 'real_estate_agency'
type = 'inşaat mühendislik'

# 5 km'yi dereceye dönüştürmek için step_size hesaplama
km_to_degree = 1 / 111  # 1 km'yi dereceye dönüştürme faktörü
distance_km = 5  # Her karenin kenar uzunluğu 5 km
step_size = distance_km * km_to_degree  # 5 km'yi dereceye dönüştür

radius = 1000 * distance_km / 2  # km yarıçap
# İstanbul'un sol üst ve sağ alt köşe koordinatları
#top_left = (41.3125, 28.0836)  # Sol üst köşe (yaklaşık)
top_left = (41.05, 28.7)  # Sol üst köşe (yaklaşık)
bottom_right = (40.8903, 29.4004)  # Sağ alt köşe (yaklaşık)

def fetch_places(location, radius, type):
    """Nearby Search ile işletmeleri getirir."""
    #url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    params = {
        "location": f"{location[0]},{location[1]}",
        "radius": radius,
        "query": type,
        "key": API_KEY
    }
    places = []
    while True:
        response = requests.get(url, params=params)
        data = response.json()
        
        # Sonuçları ekle
        places.extend(data.get('results', []))

        # Pagination token'ı kontrol et
        next_page_token = data.get('next_page_token')
        if not next_page_token:
            break
        
        # Token'ın aktif olması için biraz bekle
        time.sleep(2)
        params['pagetoken'] = next_page_token
    return places

def fetch_place_details(place_id):
    """Place Details API ile işletme detaylarını getirir."""
    url = f"https://maps.googleapis.com/maps/api/place/details/json"
    params = {
        "place_id": place_id,
        "fields": "name,formatted_address,formatted_phone_number,website,opening_hours,rating,review,user_ratings_total",
        "key": API_KEY
    }
    response = requests.get(url, params=params)
    return response.json().get('result', {})

def create_grid(nw, se, step):
    """İstanbul'u karelere böler ve her karenin merkezi için koordinatları döner."""
    lat = nw[0]
    lon = nw[1]
    
    coordinates = []
    
    # Sol üstten sağ alta doğru her bir kare için
    while lat > se[0]:
        lon = nw[1]  # Boylamı sıfırla
        while lon < se[1]:
            # Kareyi tanımlamak için merkez koordinatını hesapla
            center_lat = lat - (step / 2)
            center_lon = lon + (step / 2)
            
            coordinates.append((center_lat, center_lon))
            
            lon += step  # Bir sonraki kareye geç
        lat -= step  # Bir sonraki enlem bandına geç

    return coordinates

def get_places_and_details(grid_coordinates, radius, type):
    all_details = []
    for coord in grid_coordinates:
        print(f"Koordinat: {coord}")
        
        # Nearby Search ile işletmeleri getir
        places = fetch_places(coord, radius, type)
        print(f"{len(places)} işletme bulundu.")
        
        for place in places:
            place_id = place['place_id']
            details = fetch_place_details(place_id)  # Detayları çek
            all_details.append(details)
            
            # İşletme detaylarını yazdır
            print(f"Place ID: {place_id}")
            print(f"Ad: {details.get('name')}")
            print(f"Adres: {details.get('formatted_address')}")
            print(f"Telefon: {details.get('formatted_phone_number')}")
            print(f"Website: {details.get('website')}")
            print()
            
            # API limitlerini zorlamamak için kısa bir bekleme
            time.sleep(1)
    return all_details

if __name__ == "__main__":
    # Grid sınırları ve işlem
    grid_coordinates = create_grid(top_left, bottom_right, step_size)
    print(len(grid_coordinates))
    # İşletme detaylarını al
    #all_business_details = get_places_and_details(grid_coordinates, radius, type)

    # Sonuçları kaydetme (JSON)
    #with open("istanbul_avrupa_emlak_detaylari.json", "w", encoding="utf-8") as file:
    #    json.dump(all_business_details, file, ensure_ascii=False, indent=4)