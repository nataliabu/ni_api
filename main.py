from flask import Flask, jsonify

DB = [
        {
            "id": 1,
            "val": "foo"
        },
        {
            "id": 2,
            "val": "bar"
        },
        {
            "id": 3,
            "val": "baz"
        }
    ]


app = Flask(__name__)

@app.route("/")
def index():
    return "Hello NI!"

@app.route("/keys", methods=["GET"])
def get_all_keys_and_values():
    return jsonify(DB)

@app.route("/keys/<int:id>", methods=["GET"])
def get_value(id):
    result = {}
    for elem in DB:
        if elem["id"] == id:
            result = jsonify(elem["val"])
            #result = jsonify({"elem": elem})
    return result

@app.route("/keys", methods=["DELETE"])
def delete_all_values():
    for elem in DB:
        elem["val"] = None
    return jsonify(DB)

if __name__ == "__main__":
    app.run()
