from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
from use_model import get_microplastic_prediction

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/api/receive_data', methods=['POST'])
def receive_data():
    data = request.json  
    print('Received data:', data)
    res=get_microplastic_prediction(round(data["lat"],5),round(data["lng"],5))
    res=str(res)
    print(res)
    return jsonify({'message': res})

if __name__ == '__main__':
    app.run(debug=True)



