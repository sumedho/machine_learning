from flask import Flask, jsonify
from functools import wraps

app = Flask(__name__)

def validate_json(*expected_args):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            json_ob = request.get_json()
            for expected_arg in expected_args:
                if expected_arg not in json_ob or json_ob.get(expected_arg) is None:
                    abort(400)
            return func(*args, **kwargs)
        return wrapper
return decorator


@app.route('/health')
@validate_json("exercise_id", "score")
def health_check():
    return Response("", status = 200)

@app.route('/ready')
def readiness_check():
    if model.is_ready():
        return Response("", status = 200)
    else:
        return Response("", status = 503)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)