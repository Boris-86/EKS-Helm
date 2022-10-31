from flask import Flask, redirect, url_for, request, render_template
from weather import seven_days_forecast
from weather import save_history

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index(city='no_city', res_dict={}):

    if request.method == 'GET':
        city = request.args.get('city')
        save_history(city)
        res_dict = seven_days_forecast(city) if city else {}
    return render_template('weather.html', city=city, resdict=res_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
