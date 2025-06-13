from flask import Flask, request, render_template_string, jsonify
import numpy as np

app = Flask(__name__)

# Dummy crop prediction dictionary
crop_dict = {
    1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya", 7: "Orange",
    8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes", 12: "Mango", 13: "Banana",
    14: "Pomegranate", 15: "Lentil", 16: "Blackgram", 17: "Mungbean", 18: "Mothbeans",
    19: "Pigeonpeas", 20: "Kidneybeans", 21: "Chickpea", 22: "Coffee"
}

# Dummy recommendation function for now
def recommendation(N, P, K, temperature, humidity, ph, rainfall):
    # This is placeholder logic – replace with actual model logic
    return "Wheat"

# HTML UI for browser-based testing
HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Crop Recommendation</title>
    <style>
        body { font-family: Arial; background: #f0f8ff; padding: 40px; }
        .form { max-width: 400px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 0 10px #ccc; }
        input { width: 100%; padding: 8px; margin: 8px 0; }
        button { background: #28a745; color: white; padding: 10px; width: 100%; border: none; border-radius: 4px; }
        h2 { text-align: center; }
        .result { margin-top: 20px; text-align: center; font-weight: bold; color: #007bff; }
    </style>
</head>
<body>
    <div class="form">
        <h2>Crop Recommendation</h2>
        <form method="POST" action="/">
            <input type="number" name="N" placeholder="Nitrogen" required>
            <input type="number" name="P" placeholder="Phosphorus" required>
            <input type="number" name="K" placeholder="Potassium" required>
            <input type="number" step="any" name="temperature" placeholder="Temperature" required>
            <input type="number" step="any" name="humidity" placeholder="Humidity" required>
            <input type="number" step="any" name="ph" placeholder="pH" required>
            <input type="number" step="any" name="rainfall" placeholder="Rainfall" required>
            <button type="submit">Predict Crop</button>
        </form>
        {% if result %}
            <div class="result">🌾 Recommended Crop: {{ result }}</div>
        {% endif %}
    </div>
</body>
</html>
'''

# HTML form route (browser use)
@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    if request.method == 'POST':
        try:
            data = {
                'N': float(request.form['N']),
                'P': float(request.form['P']),
                'K': float(request.form['K']),
                'temperature': float(request.form['temperature']),
                'humidity': float(request.form['humidity']),
                'ph': float(request.form['ph']),
                'rainfall': float(request.form['rainfall'])
            }
            result = recommendation(**data)
        except Exception as e:
            result = f"Error: {e}"
    return render_template_string(HTML, result=result)

# JSON API route for Android app
@app.route('/api', methods=['POST'])
def api_recommend():
    try:
        data = request.get_json()
        N = float(data['N'])
        P = float(data['P'])
        K = float(data['K'])
        temperature = float(data['temperature'])
        humidity = float(data['humidity'])
        ph = float(data['ph'])
        rainfall = float(data['rainfall'])

        result = recommendation(N, P, K, temperature, humidity, ph, rainfall)
        return jsonify({"recommendation": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Start server on all interfaces so Android emulator can connect
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
