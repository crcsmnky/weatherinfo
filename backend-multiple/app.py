import os
import json

from flask import Flask, request, jsonify
from pyowm import OWM

app = Flask(__name__)
app.secret_key = '3c0716f88780d6d642330dfa3c96dbca' # md5 -s incremental-istio
owm = OWM(os.environ.get('OWM_API_KEY'))

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
    locations = [
        "Austin, TX, US",
        "San Francisco, CA, US",
        "Seattle, WA, US",
        "New York, NY, US"
    ]
    ret = []

    for loc in locations:
        obs = owm.weather_at_place(loc)
        w = obs.get_weather()
        temp = w.get_temperature('fahrenheit')
        conditions = {
            'location': loc,
            'temp_cur': temp['temp'],
            'temp_min': temp['temp_min'],
            'temp_max': temp['temp_max'],
            'status': w.get_status(),
            'clouds': w.get_clouds(),
            'icon': 'http://openweathermap.org/img/w/{}.png'.format(w.get_weather_icon_name())
        }
        ret.append(conditions)

    return jsonify(ret)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
    