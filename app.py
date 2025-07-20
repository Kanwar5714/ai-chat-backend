from flask import Flask, request, jsonify
from flask_cors import CORS
from sentiment import analyze_sentiment  # uses TextBlob (optional override)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Health check route
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Flask backend is running"}), 200

# Sentiment analysis route
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()
        message = data.get("message", "").strip()

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Use TextBlob-based analysis if available, fallback to keywords
        try:
            sentiment = analyze_sentiment(message)
        except Exception as e:
            print(f"Error using TextBlob: {e}")
            message_lower = message.lower()
            positive_keywords = [
                "good", "great", "awesome", "happy", "love", "excellent",
                "amazing", "excited", "fantastic", "wonderful"
            ]
            negative_keywords = [
                "bad", "terrible", "awful", "sad", "hate", "angry",
                "disappointed", "worried", "horrible"
            ]
            if any(word in message_lower for word in positive_keywords):
                sentiment = "Positive"
            elif any(word in message_lower for word in negative_keywords):
                sentiment = "Negative"
            else:
                sentiment = "Neutral"

        return jsonify({"sentiment": sentiment}), 200

    except Exception as e:
        print(f"Error during sentiment analysis: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
