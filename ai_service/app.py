from flask import Flask, request, jsonify
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/predict": {"origins": "http://localhost:8000"}})

# Load Hugging Face text-generation pipeline
suggestion_pipeline = pipeline("text-generation", model="gpt2")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        coin = data.get("coin")
        prices = data.get("prices", [])

        if not coin or not prices:
            return jsonify({"error": "coin and prices are required"}), 400

        # Create a simple prompt for the AI model
        #prompt = (
         #   f"The last 10 prices of {coin} are {prices}. "
          #  f"Suggest whether to buy, sell, or hold {coin}."
        #)

        prompt = f"Give me a simple suggestion for {coin}, the cryptocurrency."
        # Generate a suggestion
        result = suggestion_pipeline(prompt, max_length=50, num_return_sequences=1)

        raw_text = result[0]["generated_text"]
        suggestion_text = raw_text.replace(prompt, "").strip()

        return jsonify({
            "coin": coin,
            "forecast": prices, 
            "suggestion": suggestion_text
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
