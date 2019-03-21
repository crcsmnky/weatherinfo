import os
import requests
import json

from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = '3c0716f88780d6d642330dfa3c96dbca' # md5 -s incremental-istio

if os.environ.get('ENABLE_TRACING', None) is not None:
    from opencensus.ext.stackdriver import trace_exporter as stackdriver_exporter
    from opencensus.ext.flask.flask_middleware import FlaskMiddleware
    from opencensus.trace import config_integration
    
    project = os.environ.get('PROJECT_ID')
    exporter = stackdriver_exporter.StackdriverExporter(project_id=project)
    exporter = stackdriver_exporter.StackdriverExporter()
    middleware = FlaskMiddleware(app, exporter=exporter)
    config_integration.trace_integrations(["requests"])

BASE_URL = 'http://{hostport}'.format(
    hostport=os.environ.get('BACKEND_HOSTPORT', 'localhost:5000')
)


@app.route('/', methods=['GET'])
def index():
    resp = requests.get(BASE_URL + '/api/weather')

    if resp.status_code is not 200:
        return render_template('index.html', cities=[], msg=resp.text)
    else:
        return render_template('index.html', cities=resp.json(), msg=None)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)