# thesportsdb.com/api/v1/json/3/searchevents.php?e=Real Madrid_vs_Valencia

# All leagues: https://thesportsdb.com/api/v1/json/3/all_leagues.php

# GET next events of a ligue: https://thesportsdb.com/api/v1/json/3/eventsnextleague.php?id=ID_DE_LA_LIGA

from flask import Flask, render_template, jsonify, request
import json
import requests  # Agrega esta línea para importar la biblioteca requests
from urllib.parse import unquote
import numpy as np

import random
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical

from utils.scraping import get_data_from_web as get_data_web


app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'


random_seed = 42
random.seed(random_seed)
np.random.seed(random_seed)
tf.random.set_seed(random_seed)



team_mapping = {
  'Real Madrid': 0,
  'Barcelona': 1,
  'Alaves' : 2,
  'Almeria' : 3,
  'Ath Bilbao' : 4,
  'Ath Madrid' : 5,
  'Betis' : 6,
  'Cadiz' : 7,
  'Celta Vigo' : 8,
  'Getafe' : 9,
  'Girona' : 10,
  'Granada' : 11,
  'Las Palmas' : 12,
  'Mallorca' : 13,
  'Osasuna' : 14,
  'Sevilla' : 15,
  'Sociedad' : 16,
  'Valencia' : 17,
  'Vallecano' : 18,
  'Villarreal' : 19,
  'Manchester United': 20
}


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


#@app.route('/api/get_last_five')
#def get_last_five(){
  #name = request.args.get()
#}


@app.route('/api/get/team_vs_team')
def get_team_vs_team():
  id_team_first = request.args.get('id_team_first')
  id_team_second = request.args.get('id_team_second')
  url_team_result = 'https://thesportsdb.com/api/v1/json/3/searchevents.php?e=' + id_team_first + "_vs_" + id_team_second
  #print(url_team_result)
  
  response = requests.get(url_team_result)
  
  data = response.json() if response.status_code == 200 else None

  return jsonify(data)

def extract_hour(time_str):
  hour, minute, second = map(int, time_str.split(':'))
  return hour + (minute / 60) + (second / 3600)

trained_model = None

@app.route('/api/train')
def send_data_to_neural():
  global trained_model
  data_json = unquote(request.args.get('data'))
  data = json.loads(data_json)
  print("****************** DATA ***************************")
  train_data = data["0"]
  predict_data = data["1"]
  print(train_data[0]['home_team'])
  print(train_data[0]['visitor_team'])
  print(train_data[0]['time'])
  print("****************** DATA TO PREDICT ***************************")
  print(predict_data['home_team'])
  print(predict_data['visitor_team'])
  print(predict_data['time'])
  print("**************************************************")

  # Separar características (X) y etiquetas (y)
  # Datos para entrenar
  X = [
    # [entry['home_goals'], entry['visitor_goals'], extract_hour(entry['time'])] # with raw time
    [entry['home_goals'], entry['visitor_goals'], entry['time']]
    for entry in train_data
  ]
  print(X)

  # Resultado esperado
  y = [
    [float(entry['home_goals']), float(entry['visitor_goals'])]
    for entry in train_data
  ]

  # Convertir a numpy array
  X = np.array(X)
  y = np.array(y)

  # Normalizar características
  X_normalized = normalize_data(X)

  # Dividir datos en conjuntos de entrenamiento y prueba
  split_index = int(len(X) * 0.8)
  X_train, X_test = X_normalized[:split_index], X_normalized[split_index:]
  y_train, y_test = y[:split_index], y[split_index:]

  # Entrenar la red neuronal para predecir goles de casa y visitante
  print("**** Empezando a entrenar ****")
  trained_model = train_neural_network(X_train, y_train)

  # Evaluar el modelo en datos de prueba
  mse = trained_model.evaluate(X_test, y_test)
  print(f'Mean Squared Error on test data: {mse}')
  #print(f'Accuracy on test data: {accuracy}')

  return predict_goals(predict_data['home_team'],predict_data['visitor_team'], predict_data['time'], mse)
  
  #return jsonify({'done': 'Trained finished'}), 200

def normalize_data(data):
  # Convertir los datos a tipo float32
  data = tf.constant(data, dtype=tf.float32)

  mean = tf.reduce_mean(data, axis=0)
  std = tf.math.reduce_std(data, axis=0)
  normalized_data = (data - mean) / std
  return normalized_data

def train_neural_network(X_train, y_train):
  model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(8, activation='relu'),
    Dense(2, activation='linear')
  ])

  #optimizer = Adam(learning_rate=0.001)
  #model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

  random.seed(random_seed)
  np.random.seed(random_seed)
  tf.random.set_seed(random_seed)

  model.compile(optimizer='adam', loss='mean_squared_error',metrics=['accuracy'])
  model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2, shuffle=False)

  return model

# Añadir una nueva ruta para hacer predicciones
@app.route('/api/predict', methods=['GET'])
def predict_goals(home_team, visitor_team, time, error_value):
  global trained_model  # Acceder a trained_model global

  # Obtener el valor numérico para cada equipo del diccionario
  home_team_encoded = team_mapping.get(home_team, -1)  # -1 si no se encuentra el equipo
  visitor_team_encoded = team_mapping.get(visitor_team, -1)

  if home_team_encoded == -1 or visitor_team_encoded == -1:
    return jsonify({'error': 'Invalid team name'}), 400

  # Normalizar características del nuevo partido
  new_match_data = np.array([[float(home_team_encoded), float(visitor_team_encoded), extract_hour(time)]], dtype=np.float32)
  new_match_normalized = normalize_data(new_match_data)


  predicted_home_goals_list = []
  predicted_visitor_goals_list = []

  #for _ in range(100):
  # Realizar la predicción con el modelo entrenado
  goals_prediction = trained_model.predict(new_match_normalized)

  # Convertir las predicciones a tipos de datos nativos de Python y agregar a las listas
  predicted_home_goals_list.append(float(goals_prediction[0][0]))
  predicted_visitor_goals_list.append(float(goals_prediction[0][1]))

  # Calcular la media de las predicciones
  average_home_goals = sum(predicted_home_goals_list) / len(predicted_home_goals_list)
  average_visitor_goals = sum(predicted_visitor_goals_list) / len(predicted_visitor_goals_list)

  print(f"Media de goles para el equipo local: {average_home_goals}")
  print(f"Media de goles para el equipo visitante: {average_visitor_goals}")



  return jsonify({
    'home_team': home_team,
    'visitor_team': visitor_team,
    'predicted_home_goals': average_home_goals * 100,
    'predicted_visitor_goals': average_visitor_goals * 100,
    'error_value' : error_value
  }), 200



@app.route('/api/web_scraping')
def get_data_web_scraping():
  #url = unquote(request.args.get('url'))
  #data = json.loads(data_json)
  print("Antes de enviar la url")
  #print(url)
  return get_data_web("")
  

if __name__ == '__main__':
  app.run(debug=True, port=8000)
