import openai
import time
import uuid
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

# Initialize a list to store API keys
api_keys = []

# Decorator to require API key
def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get('X-API-KEY') and request.headers.get('X-API-KEY') in api_keys:
            return f(*args, **kwargs)
        else:
            # Return a JSON response with key, status, and time instead of error message
            new_key = str(uuid.uuid4().hex)
            start_time = time.time()
            time.sleep(1)  # Simulate runtime
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            response = {
                "key": new_key,
                "status": "success",
                "time": duration
            }
            return jsonify(response), 403
    return decorated_function

# Route to generate a new API key and return the runtime
@app.route('/generate-key', methods=['GET'])
def generate_api_key():
    # Generate a new API key without dashes
    new_key = str(uuid.uuid4().hex)
    api_keys.append(new_key)

    # Measure the runtime of the API key generation process
    start_time = time.time()
    # Create a temporary delay to simulate runtime
    time.sleep(0.0001)  # Wait for 0.0001 second, you can adjust this time as needed
    end_time = time.time()
    duration = round(end_time - start_time, 2)  # Round the runtime to 2 decimal places

    # Return a JSON response with the new API key and the runtime
    response = {
        "key": new_key,
        "status": "success",
        "time": duration
    }
    return jsonify(response)

# Main route requires API key and returns data
@app.route('/', methods=['GET'])
@require_api_key
def get_data():
    url = request.args.get('url')
    if url:
        data = {"url": url}
        return jsonify(data)
    else:
        # Instead of returning an error message, return an empty response with status 400
        return jsonify(), 400

if __name__ == '__main__':
    # Run the Flask app with localhost IP and port 5000
    app.run(host='127.0.0.1', port=5000, debug=True)
