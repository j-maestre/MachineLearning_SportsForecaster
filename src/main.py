# thesportsdb.com/api/v1/json/3/searchevents.php?e=Real Madrid_vs_Valencia

# All leagues: https://thesportsdb.com/api/v1/json/3/all_leagues.php

# GET next events of a ligue: https://thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=ID_DE_LA_LIGA

from flask import Flask, render_template
import requests  # Agrega esta línea para importar la biblioteca requests

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'



@app.route('/')
def hola_mundo():
  url_leagues = 'https://thesportsdb.com/api/v1/json/3/all_leagues.php'
  response_leagues = requests.get(url_leagues)
  data = response_leagues.json() if response_leagues.status_code == 200 else None 

  return render_template('index.html', data=data)

@app.route('/liga/<name>')
def mostrar_liga(name):
  # Aquí deberías tener lógica para obtener detalles específicos de la liga con el ID proporcionado
  url_leagues = 'https://thesportsdb.com/api/v1/json/3/search_all_teams.php?l='+name
  response_leagues = requests.get(url_leagues)
  data = response_leagues.json() if response_leagues.status_code == 200 else None
  print(data) 
  return render_template('liga.html', detalles_liga=data)

if __name__ == '__main__':
  app.run(debug=True, port=8000)



