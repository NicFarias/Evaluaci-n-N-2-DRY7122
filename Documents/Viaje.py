import requests
import time

# Configuración inicial
API_KEY = "7ed3094e-f314-41b0-8e97-b0bd0154d0d1" # Reemplaza con tu token de laboratorio
BASE_URL = "https://graphhopper.com/api/1/route"
GEO_URL = "https://graphhopper.com/api/1/geocode"
CONSUMO_POR_100KM = 8.0 # Litros cada 100km

def obtener_coordenadas(ciudad):
    params = {"q": ciudad, "key": API_KEY}
    response = requests.get(GEO_URL, params=params).json()
    if 'hits' in response and len(response['hits']) > 0:
        point = response['hits'][0]['point']
        return point['lat'], point['lng']
    return None

def calcular_ruta(origen, destino):
    coord_origen = obtener_coordenadas(origen)
    coord_destino = obtener_coordenadas(destino)

    if not coord_origen or not coord_destino:
        print("Error: No se pudieron encontrar las ciudades.")
        return

    params = {
        "point": [f"{coord_origen[0]},{coord_origen[1]}", f"{coord_destino[0]},{coord_destino[1]}"],
        "vehicle": "car",
        "key": API_KEY,
        "locale": "es"
    }

    resp = requests.get(BASE_URL, params=params).json()
    
    if "paths" in resp:
        path = resp["paths"][0]
        distancia_km = path["distance"] / 1000
        tiempo_ms = path["time"]
        
        # Conversión de tiempo
        segundos = int((tiempo_ms / 1000) % 60)
        minutos = int((tiempo_ms / (1000 * 60)) % 60)
        horas = int((tiempo_ms / (1000 * 60 * 60)))
        
        combustible = (distancia_km * CONSUMO_POR_100KM) / 100

        print(f"\n--- Resultados del Viaje ---")
        print(f"Distancia: {distancia_km:.2f} km")
        print(f"Duración: {horas}h {minutos}m {segundos}s")
        print(f"Combustible estimado: {combustible:.2f} litros")
        print("-" * 30)
    else:
        print("Error al obtener la ruta.")

def main():
    while True:
        origen = input("\nIngrese 'q' para salir o Ciudad de Origen: ")
        if origen.lower() == 'q': break
        destino = input("Ingrese Ciudad de Destino: ")
        
        calcular_ruta(origen, destino)

if __name__ == "__main__":
    main()