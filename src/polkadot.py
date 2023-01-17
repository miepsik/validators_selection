from flask import Flask, send_from_directory, request

import numpy as np
import pandas as pd
from scipy.optimize import linprog
from scipy.stats import spearmanr

from collections import Counter
import os
import random

from sklearn.preprocessing import StandardScaler

from sklearn.neighbors import KDTree

from skopt import gp_minimize

import os

from UTA import UTA
from Cache import Cache
from Selector import Selector


def precompute(selector, depth, cache):
    options = np.zeros(depth)
    # for each possible path find next question
    for i in range(2 ** depth):
        model = UTA(df, negative=["Commission (in %)", "Total Stake (in DOT)"],
                    not_monotonic=["Voters", "Cluster Size"], n_probes=250, goal_function='average',
                    n_points=4, additional_points={"Commission (in %)": {-0.5: "left none"}})
        for k in range(depth):
            if k < 1:
                history = []
            q = cache.query(history)
            if q is None:
                a, b = selector.select(model)
            else:
                a, b = q
            if options[k] > 0:
                a, b = b, a
            cache.add(history, (a, b))
            model.addBetter(a, b)
            if k == 0:
                history = []
            history += [(a.tolist(), b.tolist())]

        k = 0
        while k < depth and options[k] == 1:
            options[k] = 0
            k += 1
        if k < depth:
            options[k] = 1


df = None

cache = Cache()
selector = Selector(df)

app = Flask(__name__)


def exportModel(model, columns):
    output = {}
    xps, yps = model.getUtilityFunctions()
    normalizer = 0
    for i in range(len(yps)):
        yps[i] -= min(yps[i])
        normalizer += max(yps[i])
    for i in range(len(yps)):
        yps[i] /= normalizer

    for i in range(len(columns)):
        output[columns[i]] = [xps[i].tolist(), yps[i].tolist()]
    return output

def prepare(values, columns):
    output = {}
    for i in range(len(columns)):
        output[columns[i]] = values[i]
    return output
        
        
@app.route("/fileupload", methods=['POST'])
def newFile():
	global df
	global cache
	global selector
	if 'validators' not in request.files:
		return "Validators file not provided", 400
	df = pd.read_csv(request.files.get('validators'))
	if len(df.columns) != 7:
		return "Invalid file structure, expected 7 columns, got " + str(len(df.columns)), 400
	df.columns = ["stash_address", "Commission (in %)", "Self Stake (in DOT)", "Total Stake (in DOT)", "Era Points", "Cluster Size", "Voters"]
	df = df.set_index("stash_address")
	depth = 7
	data = request.form
	if 'depth' in data:
		depth = int(data['depth'])
	cache = Cache()
	selector = Selector(df)
	precompute(selector, depth, cache)
	return "Done"


@app.route("/next", methods=['POST'])
def next():
    global cache
    data = request.json
    if 'history' in data:
        history = data['history']
    else:
        history = []
    
    if len(history) < 1: history = []
    # model creating
    model = UTA(df, negative=["Commission (in %)", "Total Stake (in DOT)"],
                    not_monotonic=["Voters", "Cluster Size"], n_probes=250, goal_function='average',
                    n_points=4, additional_points={"Commission (in %)": {-0.5: "left none"}})
    # building a model based on a history
    for (a, b) in history:
        model.addBetter(a, b)
    # searching for a new question
    q = cache.query(history)
    if q is None:
        q = selector.select(model)   
    a, b = q
    if len(history) < 1:
        quality = -1
        exported = []
    else:
    	quality = model.getPrecision();exported = exportModel(model, df.columns)
    return {"validatorA": {'values': prepare(a, df.columns), 'history': [[a.tolist(), b.tolist()]] + history}, 
            "validatorB": {'values': prepare(b, df.columns), 'history': [[b.tolist(), a.tolist()]] + history}, "quality": quality, "model": exported}
            
@app.route("/ranking", methods=['POST'])
def ranking():
    global df
    data = request.json
    if 'model' not in data:
        return "Model not provided", 400
    model = data['model']
    output = df.copy()
    output['score'] = 0
    for col in df.columns:
        if col not in model:
            return col + " not present in the model", 400
        output.score += np.interp(df[col], model[col][0], model[col][1])
    return output[['score']].to_csv()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=14237)
