from flask import Flask, jsonify
from flask_cors import CORS

from read_json_file import read_json_file

app = Flask(__name__)
CORS(app)  # cho phép mọi origin truy cập

@app.route("/api/get_json")
def get_json():
    # giả sử file test.json nằm cùng folder backend
    data = read_json_file("/Users/phamphuonghong/learnCode/VioDetect/be/data_for_frontend.json")
    return jsonify(data)

if __name__ == "__main__":
    print("✅ Flask app is starting...")
    app.run(debug=True)
