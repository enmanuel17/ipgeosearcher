from flask import request
from flask import jsonify
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
import requests
import os

app = Flask(__name__)

bootstrap = Bootstrap(app)

def get_ip_geo_data(ip):
    """
    Gets ip address geo data in json format
    """
    response = requests.get(
    'http://api.ipstack.com/{}?'.format(ip),
    params={'access_key': os.environ['geo_key']},
    return response.json()
)


def get_real_ip():
    """
    Gets the real IP behind the reverse proxy aka the real user IP
    """
    
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/')
def index():
    return render_template('index.html')

    
@app.route('/get_proxy_ip', methods=["GET"])
def get_proxy_ip():
    """
    Gets the IP of the reserver proxy server
    """
    return render_template('proxy_ip.html', ip_data=request.remote_addr), 200


@app.route('/get_ip', methods=['GET'])
def get_ip():
    """
    Gets the IP of the user that made the request, the one behind the reverse proxy
    """
    return render_template('ip_data.html', ip=get_real_ip()), ip_data=get_ip_geo_data(get_real_ip()), 200


@app.route('/get_json_ip', methods=['GET'])
def get_json_ip():
    """
    Gets the jsonify version of the reverse proxy IP, aka get_ip jsonify
    """
    return jsonify({'ip': get_real_ip()}), 200


if __name__ == '__main__':
    app.run()





