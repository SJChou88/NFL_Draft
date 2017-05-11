import flask
from sklearn.linear_model import LogisticRegression
import numpy as np
import pandas as pd

#---------- MODEL IN MEMORY ----------------#

df = pd.read_pickle('wr_data.pkl')

max_of = []
min_of =[]
cols = ['height','weight','forty','vertical','receptions','rec_yards','rec_td']
#Drop 0s and percentile everything.
for col in cols:
    df = df[df[col] != 0]
    max_of.append(df[col].max())
    min_of.append(df[col].min())
    df[col] = (df[col]-df[col].min())/(df[col].max()-df[col].min())

df['intercept']=1

X = df[['intercept','height','weight','forty','vertical','receptions','rec_yards','rec_td']]
Y = df['firstround']
PREDICTOR = LogisticRegression(class_weight='balanced').fit(X,Y)


#---------- URLS AND WEB PAGES -------------#

# Initialize the app
app = flask.Flask(__name__)

# Homepage
@app.route("/")
def viz_page():
    """
    Homepage: serve our visualization page, awesome.html
    """
    with open("awesome.html", 'r') as viz_file:
        return viz_file.read()

# Get an example and return it's score from the predictor model
@app.route("/score", methods=["POST"])
def score():
    """
    When A POST request with json data is made to this uri,
    Read the example from the json, predict probability and
    send it with a response
    """
    # Get decision score for our example that came with the request
    data = flask.request.json
    print(data)
    # Holding intercept, height, and weight constant
    variables = [1,1,1]
    cols2 =['forty','vertical','receptions','rec_yards','rec_td']
    for i in range(0,len(cols2)):
        j = i + 2
        variables.append((data["example"][i]-min_of[j])/(max_of[j] - min_of[j]))

    x = np.matrix(variables)
    score = PREDICTOR.predict_proba(x)
    # Put the result in a nice dict so we can send it as json
    results = {"score": score[0,1]}
    return flask.jsonify(results)

#--------- RUN WEB APP SERVER ------------#

# Start the app server on port 80
# (The default website port)
app.run(host='0.0.0.0', debug=True)
