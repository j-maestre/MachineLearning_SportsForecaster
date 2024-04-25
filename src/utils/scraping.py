import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify


def get_data_from_web(url):
    print("*********** URL WEB SCRAPING ***********")
    url = "https://es.fcstats.com/club,partidos,real-madrid,345,73989.php"
    print(url)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Realizar la solicitud HTTP GET
    response = requests.get(url, headers=headers)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        print("BOMBA")
        # Parsear el HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encontrar todos los elementos de fila de partido
        partidos = soup.find_all('tr', class_='matchRow')

        #print(partidos)
        partidos_totales = []

        # Iterar sobre cada fila de partido
        for partido in partidos:
            # Extraer la fecha del partido
            fecha = partido.find('td', class_='matchDate').text.strip()

            # Extraer el nombre del equipo local y su posición si está presente
            equipo_local_element = partido.find('td', class_='teamHomeName')
            equipo_local_nombre = equipo_local_element.text.strip()
            equipo_local_posicion = equipo_local_element.find('span', class_='teamPosition')
            if equipo_local_posicion:
                equipo_local_posicion = equipo_local_posicion.text.strip()
                equipo_local_nombre = equipo_local_nombre.replace(equipo_local_posicion, '')
            
            # Extraer el nombre del equipo visitante y su posición si está presente
            equipo_visitante_element = partido.find('td', class_='teamAwayName')
            equipo_visitante_nombre = equipo_visitante_element.text.strip()
            equipo_visitante_posicion = equipo_visitante_element.find('span', class_='teamPosition')
            if equipo_visitante_posicion:
                equipo_visitante_posicion = equipo_visitante_posicion.text.strip()
                equipo_visitante_nombre = equipo_visitante_nombre.replace(equipo_visitante_posicion, '')
            
            # Extraer el resultado del partido
            resultado = partido.find('td', class_='matchResult').text.strip()
            goles_equipo_local, goles_equipo_visitante = resultado.split(':')
            goles_equipo_local = int(goles_equipo_local)
            goles_equipo_visitante = int(goles_equipo_visitante)    


            # Coger la hora

            enlace_elemento = partido.find('td', class_='showMatchInfo').find('a')

            # Extraer la URL del enlace
            if enlace_elemento:
                enlace_partido = "https://es.fcstats.com/" + enlace_elemento['href']
            else:
                enlace_partido = None

            print(f"Enlace del partido: {enlace_partido}")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            # Realizar la solicitud HTTP GET
            response_time = requests.get(enlace_partido, headers=headers)

            # Después de realizar la solicitud HTTP GET al enlace del partido y obtener la respuesta en response_partido
            soup_partido = BeautifulSoup(response_time.content, 'html.parser')

            # Encontrar el elemento <div> que contiene la información de la fecha y hora del encuentro
            fecha_hora_div = soup_partido.find('div')

            # Extraer el texto dentro del elemento <a>, que contiene la información de la fecha y hora del encuentro
            fecha_hora_texto = fecha_hora_div.find('a').text.strip()

            # Separar el texto para obtener la hora del encuentro
            hora_encuentro = fecha_hora_texto.split(',')[2].strip()

            # Imprimir la hora del encuentro
            print(f"Hora del Encuentro: {hora_encuentro}")





            # hay que entrar al link y coger la fecha
            partido_formated = {
                "fecha": fecha,
                "home_name": equipo_local_nombre,
                "posicion_local": equipo_local_posicion,
                "visitor_name": equipo_visitante_nombre,
                "posicion_visitante": equipo_visitante_posicion,
                "home_goals": goles_equipo_local,
                "visitor_goals": goles_equipo_visitante
            }
            partidos_totales.append(partido_formated)

            # Imprimir los detalles del partido
            print(f"Fecha: {fecha}, Equipo Local: {equipo_local_nombre}, Posición Local: {equipo_local_posicion}, Equipo Visitante: {equipo_visitante_nombre}, Posición Visitante: {equipo_visitante_posicion}, Resultado: {resultado}")
    else:
        print("La solicitud no fue exitosa. Código de estado:", response.status_code)

    return jsonify({
        'result': partidos_totales
    }), 200


