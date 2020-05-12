from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Cocacola1!@localhost/weatherApp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        self.name = name


@app.route('/')
def index():
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=31871efdffbae59febf245aed9f2e00b'
    cities = City.query.all()
    print(cities)
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()

        weather = {
            'city': city.name,
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon']
        }

        weather_data.append(weather)
    # print(weather)

    return render_template('weather.html', weather_data=weather_data)


@app.route('/addcity', methods=['POST'])
def addcity():
    if request.method == 'POST':
        city = request.form['inputCity']

        my_data = City(city)

        db.session.add(my_data)
        db.session.commit()

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
