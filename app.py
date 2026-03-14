from flask import Flask

# This creates our actual "waiter" (the Flask web app)
app = Flask(__name__)

# This tells Flask what to do when someone goes to the main homepage ("/")
@app.route('/')
def home():
    return "🚀 Your Fake Currency Detector Web Server is Running!"

# This block actually starts the server when we run the file
if __name__ == '__main__':
    # debug=True means the server will automatically update if we change the code!
    app.run(debug=True)