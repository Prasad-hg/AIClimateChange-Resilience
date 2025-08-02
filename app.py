from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from datetime import datetime
import joblib
import numpy as np
import pandas as pd
import os
import warnings
import plotly.express as px
import plotly.io as pio
import folium
from folium.plugins import HeatMap

warnings.filterwarnings("ignore")

app = Flask(__name__)
app.secret_key = 'climate'

# ---- DATABASE CONNECTION ----
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2003",
        database="WEATHER"
    )

# ---- STATIC MODELS PATH ----
models_base_dir = os.path.join(os.path.dirname(__file__), 'models')

india_models_dir = os.path.join(models_base_dir, 'india')
india_models = {
    "regression_model": joblib.load(os.path.join(india_models_dir, 'weather_regression_model.pkl')),
    "classification_model": joblib.load(os.path.join(india_models_dir, 'weather_classification_model.pkl')),
    "location_encoder": joblib.load(os.path.join(india_models_dir, 'location_encoder.pkl')),
    "weather_encoder": joblib.load(os.path.join(india_models_dir, 'weather_encoder.pkl'))
}

world_models_dir = os.path.join(models_base_dir, 'world')
world_models = {
    "regression_model": joblib.load(os.path.join(world_models_dir, 'unified_regression_model.pkl')),
    "classification_model": joblib.load(os.path.join(world_models_dir, 'classification_model.pkl')),
    "label_encoder": joblib.load(os.path.join(world_models_dir, 'label_encoder.pkl')),
    "scaler": joblib.load(os.path.join(world_models_dir, 'scaler.pkl')),
    "weather_condition_encoder": joblib.load(os.path.join(world_models_dir, 'weather_condition_encoder.pkl'))
}

# ---- ROUTES ----

@app.route('/')
def login():
    return render_template("auth.html")
@app.route('/add_users', methods=['POST'])
def add_users():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    conn = connect_to_db()
    cursor = conn.cursor()

    # ✅ Check if username or email already exists
    cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()
        return "Username or Email already exists. Please choose another one."

    # ✅ Proceed with inserting user
    cursor.execute("""
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
    """, (username, email, password))

    conn.commit()

    session['user_id'] = cursor.lastrowid
    session['user_name'] = username
    session['user_email'] = email

    cursor.close()
    conn.close()

    return render_template("successful.html")


@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('username')
    password = request.form.get('password')

    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, email FROM users WHERE email = %s AND password_hash = %s", (email, password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        session['user_id'] = user[0]
        session['user_name'] = user[1]
        session['user_email'] = user[2]
        return redirect('/starter')
    else:
        flash('Invalid email or password', 'danger')
        return redirect('/')

@app.route('/starter')
def starter():
    name = session.get('user_name')
    if name:
        return render_template("index.html", name=name)
    else:
        flash('Please log in first.', 'warning')
        return redirect('/')

@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html', countries=world_models["label_encoder"].classes_)

@app.route('/predict', methods=['POST'])
def predict():
    location = request.form['location']
    date = request.form['date']
    try:
        location_encoded = india_models["location_encoder"].transform([location])[0]
        year = pd.to_datetime(date).year
        month = pd.to_datetime(date).month
        input_data = np.array([[location_encoded, year, month]])

        prediction_reg = india_models["regression_model"].predict(input_data)
        prediction_class = india_models["classification_model"].predict(input_data)

        temperature, humidity, precipitation, wind_speed = prediction_reg[0]
        weather_forecast = india_models["weather_encoder"].inverse_transform(prediction_class)[0]

        result = {
            "Temperature": round(temperature, 2),
            "Humidity": round(humidity, 2),
            "Precipitation": round(precipitation, 2),
            "Wind Speed": round(wind_speed, 2),
            "Weather Forecast": weather_forecast
        }
        return render_template('index.html', result=result, countries=world_models["label_encoder"].classes_)
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('index'))

@app.route('/global-predict', methods=['POST'])
def global_predict():
    country = request.form['country']
    date = request.form['date']
    try:
        country_encoded = world_models["label_encoder"].transform([country])[0]
        year, month, day = map(int, date.split('-'))
        input_features = world_models["scaler"].transform([[country_encoded, year, month, day]])

        regression_predictions = world_models["regression_model"].predict(input_features)
        classification_prediction = world_models["classification_model"].predict(input_features)[0]
        weather_condition = world_models["weather_condition_encoder"].inverse_transform([classification_prediction])[0]

        global_result = {
            "Temperature": round(regression_predictions[0, 0], 2),
            "Humidity": round(regression_predictions[0, 1], 2),
            "Precipitation": round(regression_predictions[0, 2], 2),
            "Wind Speed": round(regression_predictions[0, 3], 2),
            "Weather Condition": weather_condition
        }
        return render_template('index.html', global_result=global_result, countries=world_models["label_encoder"].classes_)
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('index'))

@app.route('/visualize')
def visualize():
    avg_temp = pd.read_csv("data/avg_temp_world.csv")
    land_temp = pd.read_csv("data/land_temp_world.csv")
    city_temp = pd.read_csv("data/city_temp.csv")

    fig1 = px.choropleth(
        avg_temp, locations='Country', locationmode='country names',
        color='AverageTemperature', title='Average Temperature by Country',
        color_continuous_scale=px.colors.sequential.Viridis
    )

    land_temp_long = land_temp.melt(id_vars=['years'], var_name='Metric', value_name='Temperature')
    fig2 = px.line(land_temp_long, x='years', y='Temperature', color='Metric',
                   title='Average Land Temperature Over Years')

    folium_map = folium.Map(location=[0, 0], zoom_start=2)
    heatmap_data = city_temp[['Latitude', 'Longitude', 'Mean_temp']].values.tolist()
    HeatMap(heatmap_data).add_to(folium_map)

    for _, row in city_temp.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"City: {row.get('City', 'Unknown')}<br>Temp: {row['Mean_temp']}°C",
            icon=folium.Icon(color='blue')
        ).add_to(folium_map)

    return render_template(
        'index1.html',
        graph1_json=pio.to_json(fig1),
        graph2_json=pio.to_json(fig2),
        folium_map_html=folium_map._repr_html_()
    )

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# ---- RUN SERVER ----
if __name__ == '__main__':
    app.run(debug=True)
