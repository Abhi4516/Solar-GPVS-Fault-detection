from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import MinMaxScaler

app = Flask(__name__)


with open('xgb.pkl', 'rb') as model_file:
    xgb_model = pickle.load(model_file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    features = {f: float(request.form[f]) for f in ['Time', 'Ipv', 'Vpv', 'Vdc', 'ia', 'ib', 'ic', 'va', 'vb', 'vc', 'Iabc', 'If', 'Vabc', 'Vf']}
    

    input_features = np.array(list(features.values())).reshape(1, -1)
    
   
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(input_features)
    

    prediction = xgb_model.predict(X_scaled)
    

    result = 'Defective' if prediction == 1 else 'Non-Defective'
    
    return render_template('prediction.html', prediction_text=f'The result of prediction is: {result}', input_features=features)

if __name__ == '__main__':
    app.run(debug=True)

