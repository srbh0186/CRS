from flask import Flask, request, render_template, jsonify
import numpy as np
import pickle
import os

# Load model and scalers
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model = pickle.load(open(os.path.join(BASE_DIR, 'model.pkl'), 'rb'))
sc = pickle.load(open(os.path.join(BASE_DIR, 'standscaler.pkl'), 'rb'))
ms = pickle.load(open(os.path.join(BASE_DIR, 'minmaxscaler.pkl'), 'rb'))

app = Flask(__name__)

# Dictionary for crop labels
crop_dict = {
    1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
    8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
    14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
    19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
}

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        N = float(request.form['Nitrogen'])
        P = float(request.form['Phosporus'])
        K = float(request.form['Potassium'])
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['Ph'])
        rainfall = float(request.form['Rainfall'])

        feature_list = [N, P, K, temp, humidity, ph, rainfall]
        single_pred = np.array(feature_list).reshape(1, -1)

        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)
        prediction = model.predict(final_features)

        crop = crop_dict.get(prediction[0], "Unknown Crop")
        result = f"{crop} is the best crop to be cultivated right there"

    except Exception as e:
        result = f"Error in prediction: {str(e)}"

    return render_template("index.html", result=result)

@app.route('/api/predict', methods=["POST"])
def api_predict():
    try:
        data = request.get_json()

        feature_list = [
            float(data['N']),
            float(data['P']),
            float(data['K']),
            float(data['temperature']),
            float(data['humidity']),
            float(data['ph']),
            float(data['rainfall'])
        ]

        single_pred = np.array(feature_list).reshape(1, -1)
        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)
        prediction = model.predict(final_features)

        crop = crop_dict.get(prediction[0], "Unknown Crop")
        return jsonify({"Recommended_Crop": crop})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "API is running"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
