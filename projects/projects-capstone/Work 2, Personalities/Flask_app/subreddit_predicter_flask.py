# api.py: your api flask application
import flask
from flask import request
import numpy as np
import pandas as pd
import pickle
from sklearn.externals import joblib

app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('subreddit_predicter.html')



@app.route('/find_subreddits',methods=["POST","GET"])
def find_subreddits():
    if request.method == 'POST':

        grouped_pred = joblib.load('pickled_grouped_pred')
        inputs = request.form
        # grabbing the parameters for this request
        c1 = request.form.get('choice_1','',type=str)
        c2 = request.form.get('choice_2','',type=str)
        c3 = request.form.get('choice_3','',type=str)
        c4 = request.form.get('choice_4','',type=str)
        c5 = request.form.get('choice_5','',type=str)
        c6 = request.form.get('choice_6','',type=str)
        c7 = request.form.get('choice_7','',type=str)
        c8 = request.form.get('choice_8','',type=str)
        c9 = request.form.get('choice_9','',type=str)
        c10 =request.form.get('choice_10','',type=str)
        choices=[c1,c2,c3,c4,c5,c6,c7,c8,c9,c10]
        new_choices=[]
        for x in choices:
            if len(x)>0:
                new_choices.append(x)
        
        return  flask.jsonify(recommender(new_choices,grouped_pred))

# app.py: your main flask application

def recommender(list_thing,subreddit_pos):
    positions=[]
    for thing in list_thing:
        if thing in subreddit_pos.index:
            positions.append(subreddit_pos.loc[thing,:])
            positions[-1]=positions[-1][:-1]
    avg_pos=[]
    for col in range(len(positions[0])):
        mean_col=[]
        for row in range(len(positions)):
            mean_col.append(positions[row][col])
        avg_pos.append(np.mean(mean_col))
    
    names=[]
    distances=[]
    for row in range(len(subreddit_pos)):
        if subreddit_pos.index[row] not in list_thing:
            names.append(subreddit_pos.index[row])
            loc=subreddit_pos.iloc[row,:-1]
            distances.append(np.sum((avg_pos-loc)**2))
    points=zip(names,distances)
    points.sort(key=(lambda x:x[1]))
    return points[:5]

@app.route('/json/<path:path>')
def send_json(path):
    return flask.send_from_directory('json', path)


if __name__ == '__main__':
    '''Connects to the server'''

    HOST = '127.0.0.1'
    PORT = '4000'
    app.run(HOST, PORT)


















