from flask import request
from flask import jsonify
from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
import requests
import os

app = Flask(__name__)

bootstrap = Bootstrap(app)

class ipData:
    def __init__(self):
        self.country = None
        self.city = None
        self.IPS = None

def get_ip_geo_data(ip):
    """
    Gets ip address geo data in json format
    """

    response = requests.get(
        'http://api.ipstack.com/{}?'.format(ip),
        params={'access_key': os.environ['geo_key']},
    )
    return response.json()


def get_real_ip():
    """
    Gets the real IP behind the reverse proxy aka the real user IP
    """
    
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return request.environ['REMOTE_ADDR']
    else:
        return request.environ['HTTP_X_FORWARDED_FOR']

@app.route('/')
def index():
    ip = get_real_ip()
    ip_data = ipData()
    geo_data = get_ip_geo_data(ip)
    ip_data.country = geo_data['country_name']
    ip_data.city = geo_data['city']
    return render_template('index.html', ip=ip, country=ip_data.country, city=ip_data.city)


@app.route('/get_json_ip', methods=['GET'])
def get_json_ip():
    """
    Gets the jsonified version of the requester's IP
    """
    return jsonify({'ip': get_real_ip()}), 200


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run()





