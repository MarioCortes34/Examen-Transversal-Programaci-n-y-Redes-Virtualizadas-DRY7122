import requests
import urllib.parse

geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"
key = "e3f2fc60-9434-4899-a11b-dabd92fea238"  # Tu API Key


def geocoding(location, key):
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_status = replydata.status_code

    if json_status == 200:
        json_data = replydata.json()
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]
        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")

        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif country:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name

        print(f"Geocoding API URL para {new_loc} (Tipo de lugar: {value})\n{url}")
    else:
        print(f"Geocode API status: {json_status}\nMensaje de error: {replydata.text}")
        lat, lng, new_loc = "null", "null", location

    return json_status, lat, lng, new_loc

# Traducción de español a los valores que acepta la API
vehiculos = {
    "auto": "car",
    "bicicleta": "bike",
    "caminando": "foot"
}

# PROGRAMA PRINCIPAL

while True:
    loc1 = input("Ciudad de Origen (o 's' para salir): ").strip()
    if loc1.lower() == "s":
        break

    orig = geocoding(loc1, key)
    if orig[0] != 200:
        continue

    loc2 = input("Ciudad de Destino (o 's' para salir): ").strip()
    if loc2.lower() == "s":
        break

    dest = geocoding(loc2, key)
    if dest[0] != 200:
        continue

    while True:
        vehiculo_input = input("Medio de transporte (auto, bicicleta, caminando): ").strip().lower()
        if vehiculo_input in vehiculos:
            vehicle = vehiculos[vehiculo_input]
            break
        else:
            print("Por favor escribe: auto, bicicleta o caminando")

    print("=================================================")
    print(f"Ruta desde {orig[3]} hasta {dest[3]}")
    print("=================================================")

    params = {
        "key": key,
        "point": [f"{orig[1]},{orig[2]}", f"{dest[1]},{dest[2]}"],
        "vehicle": vehicle,
        "locale": "es",
        "instructions": "true"
    }

    paths_reply = requests.get(route_url, params=params)
    paths_status = paths_reply.status_code

    if paths_status == 200:
        paths_data = paths_reply.json()
        distance_km = paths_data["paths"][0]["distance"] / 1000
        distance_mi = distance_km / 1.60934
        time_ms = paths_data["paths"][0]["time"]
        sec = int(time_ms / 1000 % 60)
        min = int(time_ms / 1000 / 60 % 60)
        hr = int(time_ms / 1000 / 60 / 60)

        print(f"Duración del viaje: {hr:02d}:{min:02d}:{sec:02d}")
        print(f"Distancia recorrida: {distance_mi:.1f} millas / {distance_km:.1f} km")
        print("=================================================")
        print("Narrativa del viaje:")
        for i, step in enumerate(paths_data["paths"][0]["instructions"]):
            print(f"{i+1}. {step['text']} ({step['distance']:.0f} m)")
        print("=================================================")
    else:
        print(f"Error al obtener ruta. Código de estado: {paths_status}")