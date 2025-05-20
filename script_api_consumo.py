import requests

API_KEY = "e9631c82-31c4-4b8f-902f-ec5586924bf6"  # Reemplaza por tu API key

def geocodificar(ciudad):
    url = f"https://graphhopper.com/api/1/geocode?q={ciudad}&limit=1&key={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        resultados = response.json()["hits"]
        if resultados:
            lat = resultados[0]["point"]["lat"]
            lon = resultados[0]["point"]["lng"]
            return f"{lat},{lon}"
        else:
            print(f"No se encontraron coordenadas para '{ciudad}'")
            return None
    else:
        print(f"Error al geocodificar. Código: {response.status_code}")
        return None

def obtener_datos(origen_coords, destino_coords):
    url = f"https://graphhopper.com/api/1/route?point={origen_coords}&point={destino_coords}&vehicle=car&locale=es&calc_points=false&key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        datos = response.json()
        distancia_km = datos["paths"][0]["distance"] / 1000
        duracion_seg = datos["paths"][0]["time"] / 1000
        horas = int(duracion_seg // 3600)
        minutos = int((duracion_seg % 3600) // 60)
        segundos = int(duracion_seg % 60)
        print(f"\nDistancia: {distancia_km:.2f} km")
        print(f"Duración: {horas}h {minutos}m {segundos}s\n")
    else:
        print(f"\nError al obtener los datos. Código: {response.status_code}")
        print("Respuesta:", response.text)

def main():
    while True:
        origen = input("Ciudad de Origen (o 'q' para salir): ")
        if origen.lower() == 'q':
            break
        destino = input("Ciudad de Destino (o 'q' para salir): ")
        if destino.lower() == 'q':
            break

        origen_coords = geocodificar(origen)
        destino_coords = geocodificar(destino)

        if origen_coords and destino_coords:
            obtener_datos(origen_coords, destino_coords)

if __name__ == "__main__":
    main()
