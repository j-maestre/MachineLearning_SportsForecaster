# thesportsdb.com/api/v1/json/3/searchevents.php?e=Real Madrid_vs_Valencia

# All leagues: https://thesportsdb.com/api/v1/json/3/all_leagues.php

# GET next events of a ligue: https://thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=ID_DE_LA_LIGA

from flask import Flask, render_template, jsonify, request
import json
import requests  # Agrega esta línea para importar la biblioteca requests
from urllib.parse import unquote


import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical


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
  #print(url_leagues) 
  return render_template('liga.html', detalles_liga=data)

# Devuelve la informacion de los ultimos 5 partidos de un equipo local en un html
@app.route('/liga/<name>/<id_team>')
def mostrar_resultados_team(name, id_team):
  url_team_result = 'https://thesportsdb.com/api/v1/json/3/eventslast.php?id='+id_team
  url_team_next_events = 'https://thesportsdb.com/api/v1/json/3/eventsnext.php?id='+id_team
  
  response = requests.get(url_team_result)
  response_next = requests.get(url_team_next_events)
  
  data = response.json() if response.status_code == 200 else None
  data_next = response_next.json() if response_next.status_code == 200 else None
  #print(data_next)
  return render_template('team.html', team=data, team_next=data_next)

# Devuelve los ultimos partidos de un equipo local
@app.route('/api/get')
def get_resultados_team():
  id_team = request.args.get('id_team')
  url_team_result = 'https://thesportsdb.com/api/v1/json/3/eventslast.php?id='+id_team
  #url_team_next_events = 'https://thesportsdb.com/api/v1/json/3/eventsnext.php?id='+id_team
  
  response = requests.get(url_team_result)
  #response_next = requests.get(url_team_next_events)
  
  data = response.json() if response.status_code == 200 else None
  #data_next = response_next.json() if response_next.status_code == 200 else None
  #print(data_next)
  return jsonify(data)

@app.route('/predict')
def predict_view():
  return render_template('predict.html')

# Devuelve todas las ligas disponibles
@app.route('/api/all_leagues')
def get_all_leagues():
  url = 'https://thesportsdb.com/api/v1/json/3/all_leagues.php'
  response = requests.get(url)
  
  if response.status_code == 200:
    data = response.json()
    #print(data)
    return jsonify(data)
  else:
    return jsonify({'error': 'Error en la solicitud a la API'}), 500

# Devuelve todos los equipos de una liga
@app.route('/api/teams_by_league')
def get_all_teams_by_leagues():
  name = request.args.get('name')
  url = 'https://thesportsdb.com/api/v1/json/3/search_all_teams.php?l='+name
  response = requests.get(url)
  print("URL-> ", url)
  
  if response.status_code == 200:
    data = response.json()
    #print(data)
    return jsonify(data)
  else:
    return jsonify({'error': 'Error en la solicitud a la API'}), 500

@app.route('/api/get/team_vs_team')
def get_team_vs_team():
  id_team_first = request.args.get('id_team_first')
  id_team_second = request.args.get('id_team_second')
  url_team_result = 'https://thesportsdb.com/api/v1/json/3/searchevents.php?e=' + id_team_first + "_vs_" + id_team_second
  #print(url_team_result)
  
  response = requests.get(url_team_result)
  
  data = response.json() if response.status_code == 200 else None

  return jsonify(data)


@app.route('/api/train')
def send_data_to_neural():
  data_json = unquote(request.args.get('data'))
  data = json.loads(data_json)
  print("****************** DATA ***************************")
  print(data[0])
  print("**************************************************")

  # Separar características (X) y etiquetas (y)
  X = [
    [entry['home_goals'], entry['visitor_goals']]
    for entry in data
  ]
  y = [1 if entry['home_goals'] > entry['visitor_goals'] else 0 for entry in data]

  # Convertir a numpy array
  X = tf.constant([[float(entry[0]), float(entry[1])] for entry in X], dtype=tf.float32)
  y = tf.constant(y, dtype=tf.float32)

  # Normalizar características
  X_normalized = normalize_data(X)

  # Dividir datos en conjuntos de entrenamiento y prueba
  split_index = int(len(X) * 0.8)
  X_train, X_test = X_normalized[:split_index], X_normalized[split_index:]
  y_train, y_test = y[:split_index], y[split_index:]

  # Entrenar la red neuronal
  trained_model = train_neural_network(X_train, y_train)

  # Evaluar el modelo en datos de prueba
  accuracy = trained_model.evaluate(X_test, y_test)[1]
  print(f'Accuracy on test data: {accuracy}')

  print(f'Accuracy on test data: {accuracy}')

def normalize_data(data):
  mean = tf.reduce_mean(data, axis=0)
  std = tf.math.reduce_std(data, axis=0)
  normalized_data = (data - mean) / std
  return normalized_data

def train_neural_network(X_train, y_train):
  model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(32, activation='relu'),
    Dense(1, activation='sigmoid')
  ])

  #optimizer = Adam(learning_rate=0.001)
  #model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

  model.compile(optimizer='adam', loss='sparse-categorical_crossentropy',metrics=['accuracy'])
  model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

  return model


if __name__ == '__main__':
  app.run(debug=True, port=8000)
