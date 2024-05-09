import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify


def get_data_from_web(url):
    print("*********** URL WEB SCRAPING ***********")

    url = "https://es.fcstats.com/club,partidos,real-madrid,345,73989.php"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        soup = BeautifulSoup(response.content, 'html.parser')
        partidos = soup.find_all('tr', class_='matchRow')

        partidos_totales = []

        # Iterate each match row
        for partido in partidos:

            fecha = partido.find('td', class_='matchDate').text.strip()

            equipo_local_element = partido.find('td', class_='teamHomeName')
            equipo_local_nombre = equipo_local_element.text.strip()
            equipo_local_posicion = equipo_local_element.find('span', class_='teamPosition')
            if equipo_local_posicion:
                equipo_local_posicion = equipo_local_posicion.text.strip()
                equipo_local_nombre = equipo_local_nombre.replace(equipo_local_posicion, '')
            
            equipo_visitante_element = partido.find('td', class_='teamAwayName')
            equipo_visitante_nombre = equipo_visitante_element.text.strip()
            equipo_visitante_posicion = equipo_visitante_element.find('span', class_='teamPosition')
            if equipo_visitante_posicion:
                equipo_visitante_posicion = equipo_visitante_posicion.text.strip()
                equipo_visitante_nombre = equipo_visitante_nombre.replace(equipo_visitante_posicion, '')
            
            resultado = partido.find('td', class_='matchResult').text.strip()
            goles_equipo_local, goles_equipo_visitante = resultado.split(':')
            goles_equipo_local = int(goles_equipo_local)
            goles_equipo_visitante = int(goles_equipo_visitante)    

            enlace_elemento = partido.find('td', class_='showMatchInfo').find('a')

            if enlace_elemento:
                enlace_partido = "https://es.fcstats.com/" + enlace_elemento['href']
            else:
                enlace_partido = None

            print(f"Enlace del partido: {enlace_partido}")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

            response_time = requests.get(enlace_partido, headers=headers)
            soup_partido = BeautifulSoup(response_time.content, 'html.parser')

            fecha_hora_div = soup_partido.find('div')
            fecha_hora_texto = fecha_hora_div.find('a').text.strip()
            hora_encuentro = fecha_hora_texto.split(',')[2].strip()

            print(f"Hora del Encuentro: {hora_encuentro}")

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

            print(f"Fecha: {fecha}, Equipo Local: {equipo_local_nombre}, Posición Local: {equipo_local_posicion}, Equipo Visitante: {equipo_visitante_nombre}, Posición Visitante: {equipo_visitante_posicion}, Resultado: {resultado}")
    else:
        print("La solicitud no fue exitosa. Código de estado:", response.status_code)

    return jsonify({
        'result': partidos_totales
    }), 200


