import os
import json

from flask import Flask, request, jsonify
from pyowm.owm import OWM
from prometheus_client import Gauge, generate_latest

app = Flask(__name__)
app.secret_key = '3c0716f88780d6d642330dfa3c96dbca' # md5 -s incremental-istio
owm = OWM(os.environ.get('OWM_API_KEY'))

city_metric = {
    'Austin, TX, US': Gauge('city_temp_austin_tx_us', 'Temperatures for Austin, TX, US'), 
    'San Francisco, CA, US': Gauge('city_temp_san_fran_ca_us', 'Temperatures for San Francisco, CA, US '),
    'Seattle, WA, US': Gauge('city_temp_seattle_wa_us', 'Temperatures for Seattle, WA, US'),
    'New York, NY, US': Gauge('city_temp_new_york_ny_us', 'Temperatures for New York, NY, US')
}

if os.environ.get('ENABLE_TRACING', None) is not None:
    from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter
    from opencensus.ext.flask.flask_middleware import FlaskMiddleware
    from opencensus.trace import config_integration
    
    project = os.environ.get('PROJECT_ID')
    exporter = stackdriver_exporter.StackdriverExporter(project_id=project)
    middleware = FlaskMiddleware(app, exporter=exporter)
    config_integration.trace_integrations(["requests"])


@app.route('/api/weather', methods=['GET'])
def current_weather():
    ret = []

    mgr = owm.weather_manager()
    for city, metric in city_metric.items():
        obs = mgr.weather_at_place(city)
        w = obs.weather
        temp = w.temperature('fahrenheit')
        conditions = {
            'location': city,
            'temp_cur': temp['temp'],
            'temp_min': temp['temp_min'],
            'temp_max': temp['temp_max'],
            'status': w.status,
            'clouds': w.clouds,
            'icon': 'http://openweathermap.org/img/w/{}.png'.format(w.weather_icon_name)
        }
        ret.append(conditions)
        metric.set(temp['temp'])

    return jsonify(ret)


@app.route('/metrics', methods=['GET'])
def metrics():
    return generate_latest()


@app.route('/version', methods=['GET'])
def version():
    return "weather-backend: multiple"



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    