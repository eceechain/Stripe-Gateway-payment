from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/")
def home():
    return "Stripe Gateway Payment!"

if __name__ == "__main__":
    app.run(debug=True)