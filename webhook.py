import json
import os
import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    print(json.dumps(req, indent=4))
    
    res = makeResponse(req)
    
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeResponse(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    city = " ".join(str(x) for x in city)
    #city = str(city)
    print(city)
    date = parameters.get("date")
    date = " ".join(str(x) for x in date)
    #date = str(date)
    r=requests.get('http://api.openweathermap.org/data/2.5/forecast?q='+city+'&appid=a6400b9f821b0fc030dede972794b8b9')
    json_object = r.json()
    print(json_object)
    weather=json_object['list']
    for i in range(0,30):
        if date in weather[i]['dt_txt']:
            condition= weather[i]['weather'][0]['description']
            break
    speech = "The weather condition in "+city+" on "+date+" is "+condition
    return {
    "speech": speech,
    "displayText": speech,
    "source": "apiai-weather-webhook"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("Starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
