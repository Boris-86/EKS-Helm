from typing import List, Any
import os
from requests import get
import json
from datetime import datetime
import random
import logging
import boto3
from botocore.exceptions import ClientError
from botocore.client import Config
gmt = 3

def seven_days_forecast(city):
    """
    A function that gets the weather forecast for the next 7 days for the requested city.
    :param city: the city to get the forecast for.
    :return: a list for 7 days with the following attr for each day: date, max temp, min temp, avg temp, humidity.
    """

    if ' ' not in city:
        city += ','

    baseurl = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/' + \
              city + \
              '/next7days?'
    params = {'unitGroup': 'metric',
              'elements': 'datetime,tempmax,tempmin,temp,humidity',
              'key': '5UNU7BCKU5MGMGA2AEVAETFS8',
              'contentType': 'json'}
    #finalurl = baseurl + params
    data = get(baseurl, params)
    status = data.status_code
    if status != 200:
        return {'status': status, 'message':"Sorry, We do not support cities on Omicron Persei 8, yet..."}
    content = json.loads(data.content)
    res_addr = content['resolvedAddress']
    curr_cond = content['currentConditions']
    days_list = [{attr: day[attr]
                  for attr in ['datetime', 'temp', 'tempmin', 'tempmax', 'humidity']}
                 for day in content['days']]
    for day in days_list:
        day['weekday'] = datetime.strptime(day['datetime'], '%Y-%m-%d').strftime('%A')
        day['datetime'] = "/".join(day['datetime'].split("-")[::-1])
    fdict = {'status': status, 'res_addr': res_addr, 'curr_cond': curr_cond, 'days': days_list}
    return fdict

def download_file(bucket_name='ex2-storage', obj_name='sky.jpg', timeout=600):
    s3_client = boto3.client('s3', aws_access_key_id, aws_secret_access_key, config=Config(signature_version='s3v4', region_name='eu-central-1'))
    try:
       response = s3_client.generate_presigned_url('get_object', Params={'Bucket': bucket_name,'Key': obj_name, 'ResponseContentType': 'binart/octet-stream'}, ExpiresIn=timeout)
    except ClientError as e:
       logging.error(e)
       return None
    return response

def save_item2db(res_add, date, day, min, max, humi, time_stamp):
    #time_now = "%s:%s:%s" % (time_stamp.hour+gmt,time_stamp.minute,time_stamp.second)
    db = boto3.resource('dynamodb', aws_access_key_id, aws_secret_access_key, region_name='eu-central-1')
    table = db.Table("weather_db")
    response = table.put_item(Item={'full_address':res_add,'date':date,'weekday':day,'tempmax':max,'tempmin':min,'humidity':humi,'time_stamp':time_stamp}) 
    return response
def save_history(city_history):

    filename = '/home/boris/infy/git_hub/EKS-Helm/history.json'
    current_date = datetime.now()
    data = {city_history: datetime.strftime(current_date, "%H:%M, %d-%b-%Y")}
    db = {"logs": []}
    if os.path.isfile(filename):
        with open(filename, "r") as file:
            temp = json.load(file)
        temp['logs'].append(data)
        with open(filename, "r+") as file:
            json.dump(temp, file, indent = 4)
    else:
        with open(filename, "w") as file:
            json.dump(db, file, indent = 4)

if __name__ == "__main__":
    print(seven_days_forecast('haifa'))


