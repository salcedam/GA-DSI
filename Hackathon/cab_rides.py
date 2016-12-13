# api.py: your api flask application
import flask
import numpy as np
import pandas as pd
import pickle
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.externals import joblib

app = flask.Flask(__name__)

@app.route('/')
def send_form():
    return app.send_static_file('taxi.html')


@app.route('/find_hist',methods=["POST","GET"])
def find_hist():
    if flask.request.method == 'POST':
        inputs = flask.request.form
        month = inputs['month'][0]
        day = inputs['day'][0]
        
        model = joblib.load('/Users/thomas/GA-DSI/Untitled Folder/Models/pickled_history')
        hourly_data={}
        for hour in range(24):
            hourly_data[hour]=float(model.loc[(int(month),int(day),int(hour)),:].values[0])
        return flask.jsonify(hourly_data)



@app.route('/find_fare',methods=["POST","GET"])
def find_fare():
    if flask.request.method == 'POST':
        inputs = flask.request.form

        # grabbing the parameters for this request
        dist = inputs['dist'][0]
        rain = inputs['rain'][0]
        temp = inputs['temp'][0]
        day =  inputs['day'][0]  # Day of week, Monday is 0 and Sunday is 6
        month= inputs['month'][0]
        pass_count= inputs['pass_count'][0]

        day_cols=[]
        for thing in range(7):
            day_cols.append(0)
        day_cols[int(day)]=1
        

        file_lookup={'7':'2015-07','8':'2015-08','9':'2015-09','10':'2015-10','11':'2015-11','12':'2015-12','1':'2016-01','2':'2016-02',\
            '3':'2016-03','4':'2016-04','5':'2016-05','6':'2016-06'}
        file_name=file_lookup[str(month)]
        model = joblib.load('/Users/thomas/GA-DSI/Untitled Folder/Models/pickled_'+file_name)
        model = joblib.load(file_name)


                ### Check the actual hour numbers, want to make sure that it doesn't start on 0, or 1. Do it correctly

            # The column orders are all screwed up
        hour_dict={'0':0,'1':1,'2':12,'3':17,'4':18,'5':19,'6':20,'7':21,'8':22,'9':"drop",'10':2,'11':3,'12':4,'13':5,'14':6,'15':7,'16':8,'17':9,'18':10,\
                            '19':11,'20':13,'21':14,'22':15,'23':16}
        
        rates_by_hour={}
        for hour in range(24):

            hour_cols=[]
            for thing in range(23):
                hour_cols.append(0)
            if hour!=9:
                # hour_cols[hour_dict[hour]]=1
                hour_cols[(hour_dict[str(hour)])]=1
                


            # objects=[float(dist),int(pass_count),float(plat),float(plon),float(dlat),float(dlon),int(temp),float(rain)]
            objects=[float(dist),int(pass_count),int(temp),float(rain)]
            objects.extend(day_cols[:-1])
            objects.extend(hour_cols)
            # rates_by_hour.append([hour,objects])
            pred_array=[x for x in objects]
            prediction=model.predict(pred_array)[0]
            rates_by_hour[hour]=prediction
        
        return  flask.jsonify(rates_by_hour)

# app.py: your main flask application

if __name__ == '__main__':
    '''Connects to the server'''

    HOST = '127.0.0.1'
    PORT = '4000'
    app.run(HOST, PORT)
