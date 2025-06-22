from flask import Flask, request, jsonify
import tensorflow as tf
import pickle
from tensorflow.keras.preprocessing.sequence import pad_sequences
from utils.preprocessing import preprocess_pipeline

# Init app
app = Flask(__name__)

# Load model & tokenizer
model = tf.keras.models.load_model("model/bilstm_model_V3_0.9727.h5")
with open("model/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Parameter padding (contoh: maxlen = 47)
MAXLEN = 47

# Mapping label angka ke nama kelas
label_mapping = {
    0: "normal",
    1: "phishing",
    2: "promo"
}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Input yang berupa list atau dict
    if isinstance(data, list):
        if len(data) == 0 or not isinstance(data[0], dict):
            return jsonify({"error": "Invalid input format. Expecting a list of JSON objects with 'text' field."}), 400
        data = data[0]  # ambil elemen pertama

    if not isinstance(data, dict) or "text" not in data:
        return jsonify({"error": "Missing 'text' field."}), 400

    raw_text = data["text"]
    preprocessed_text = preprocess_pipeline(raw_text)

    # Tokenisasi & padding
    seq = tokenizer.texts_to_sequences([preprocessed_text])
    padded = pad_sequences(seq, maxlen=MAXLEN, padding='post', truncating='post')

    # Prediksi probabilitas untuk tiap kelas
    prediction_probs = model.predict(padded)[0]  # contoh output: [0.1, 0.7, 0.2]

    # Tentukan kelas dengan probabilitas tertinggi
    predicted_label_index = prediction_probs.argmax()
    predicted_label_name = label_mapping[predicted_label_index]
    prediction_score = float(prediction_probs[predicted_label_index])

    return jsonify({
        "input_text": raw_text,
        "preprocessed_text": preprocessed_text,
        "prediction_scores": prediction_probs.tolist(),
        "prediction_score": prediction_score,
        "label": predicted_label_name
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)