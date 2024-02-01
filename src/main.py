# thesportsdb.com/api/v1/json/3/searchevents.php?e=Real Madrid_vs_Valencia

# All leagues: https://thesportsdb.com/api/v1/json/3/all_leagues.php

# GET next events of a ligue: https://thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=ID_DE_LA_LIGA

from flask import Flask, render_template, jsonify, request
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
  print(url_leagues) 
  return render_template('liga.html', detalles_liga=data)



@app.route('/liga/<name>/<id_team>')
def mostrar_resultados_team(name, id_team):
  url_team_result = 'https://thesportsdb.com/api/v1/json/3/eventslast.php?id='+id_team
  url_team_next_events = 'https://thesportsdb.com/api/v1/json/3/eventsnext.php?id='+id_team
  
  response = requests.get(url_team_result)
  response_next = requests.get(url_team_next_events)
  
  data = response.json() if response.status_code == 200 else None
  data_next = response_next.json() if response_next.status_code == 200 else None
  print(data_next)
  return render_template('team.html', team=data, team_next=data_next)

@app.route('/predict')
def predict_view():
  return render_template('predict.html')

@app.route('/api/all_leagues')
def get_all_leagues():
  url = 'https://thesportsdb.com/api/v1/json/3/all_leagues.php'
  response = requests.get(url)
  
  if response.status_code == 200:
    data = response.json()
    print(data)
    return jsonify(data)
  else:
    return jsonify({'error': 'Error en la solicitud a la API'}), 500

@app.route('/api/teams_by_league')
def get_all_teams_by_leagues():
  name = request.args.get('name')
  url = 'https://thesportsdb.com/api/v1/json/3/search_all_teams.php?l='+name
  response = requests.get(url)
  print("URL-> ", url)
  
  if response.status_code == 200:
    data = response.json()
    print(data)
    return jsonify(data)
  else:
    return jsonify({'error': 'Error en la solicitud a la API'}), 500

    

if __name__ == '__main__':
  app.run(debug=True, port=8000)
