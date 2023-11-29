from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__,template_folder="template") 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///location.db'
db = SQLAlchemy(app)  

class Datapoint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    aqi = db.Column(db.Float)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/location', methods=['POST'])
def add_location():
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    api_url = "https://api.waqi.info/feed/geo:+"+latitude+";"+longitude+"/?token=a82668d29bbf0df2588bf99480928eae2001cad7"  
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
    location = Datapoint(latitude=latitude, longitude=longitude, aqi=data['data']['aqi'])
    db.session.add(location)
    db.session.commit()
    return 'Location added successfully'

@app.route('/location', methods=['GET'])
def get_location():
    locations = Datapoint.query.all()
    location_list = []
    for location in locations:
        location_dict = {'lat': location.latitude, 'lon': location.longitude, 'aqi': location.aqi}
        location_list.append(location_dict)
    return render_template('mapa.html', locations=location_list)

# @app.route('/open', methods=['POST'])
# def fetch_AQI():

#     api_url = "https://api.waqi.info/feed/here/?token=a82668d29bbf0df2588bf99480928eae2001cad7"  
#     response = requests.get(api_url)
#     if response.status_code == 200:
#         data = response.json()
#     aqi=data['data']['aqi']
#     aqi = AQI(aqi=aqi)
#     db.session.add(aqi)
#     db.session.commit()
#     return "aqi added successfully"


@app.route('/map', methods=['GET'])
def get_map():

    forecast_api_url="https://api.waqi.info/feed/geo:53.3;-6.2/?token=a82668d29bbf0df2588bf99480928eae2001cad7"
    response = requests.get(forecast_api_url)
    if response.status_code == 200:
        data = response.json()
        
    return render_template('map.html')

# @app.route('/map', methods=['GET'])
# def get_map():
#     api_url = "https://api.waqi.info/v2/map/bounds?latlng=53.350140,-6.266155,54.3,-6.8&networks=all&token=a82668d29bbf0df2588bf99480928eae2001cad7"
#     return render_template('map.html')

# @app.route('/open', methods=['GET'])
# def get_AQI():
#     aqis = AQI.query.all()
#     aqi_list = []
#     for aqi in aqis:
#         aqi_dict = {'aqi': aqi.aqi}
#         aqi_list.append(aqi_dict)
#     return {'aqis': aqi_list}


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
