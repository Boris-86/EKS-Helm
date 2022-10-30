from flask import Flask, redirect, url_for, request, render_template
from weather import seven_days_forecast
from weather import download_file
from weather import save_item2db
import requests
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index(city='no_city', res_dict={}):
    img = download_file()
    if request.method == 'GET':
        city = request.args.get('city')
        if city:
          res_dict = seven_days_forecast(city)
          if res_dict['status'] == 200:
             for i in range(0,7):
               save_item2db( res_dict['res_addr'], res_dict['days'][i]['datetime'], res_dict['days'][i]['weekday'], str(res_dict['days'][i]['tempmin']), str(res_dict['days'][i]['tempmax']),str(res_dict['days'][i]['humidity']), str(datetime.now()))
        else:
          {}
    return render_template('weather.html', city=city, resdict=res_dict, image = img)



if __name__ == '__main__':
    app.run(host='0.0.0.0')
