from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# Model file paths
def get_model_path(name):
    return os.path.join('models', name)

MODELS = {
    'AdaBoost': get_model_path('adaboost_model.pkl'),
    'Decision Tree': get_model_path('decision_tree_model.pkl'),
    'Gaussian NB': get_model_path('gaussian_nb_model.pkl'),
    'Gradient Boosting': get_model_path('gradient_boosting_model.pkl'),
    'KNN': get_model_path('knn_model.pkl'),
    'Logistic Regression': get_model_path('logistic_regression_model.pkl'),
    'Random Forest': get_model_path('random_forest_model.pkl'),
    'SVM': get_model_path('svm_model.pkl'),
    'XGBoost': get_model_path('xgboost_model.pkl'),
}

# Load models once at startup
loaded_models = {}
for name, path in MODELS.items():
    with open(path, 'rb') as f:
        loaded_models[name] = pickle.load(f)

@app.route('/', methods=['GET', 'POST'])
def index():
    predictions = {}
    if request.method == 'POST':
        try:
            rsrp = float(request.form['rsrp'])
            rsrq = float(request.form['rsrq'])
            snr = float(request.form['snr'])
            features = [[rsrp, rsrq, snr]]
            label_map = {
                0: 'Excellent',
                1: 'Good',
                2: 'Moderate',
                3: 'Poor',
            }
            for name, model in loaded_models.items():
                try:
                    pred = model.predict(features)
                    label = label_map.get(pred[0], str(pred[0]))
                    predictions[name] = label
                except Exception as e:
                    predictions[name] = f'Error: {e}'
        except Exception as e:
            predictions = {name: f'Input error: {e}' for name in loaded_models}
    return render_template('index.html', predictions=predictions)

if __name__ == '__main__':
    app.run(debug=True)
