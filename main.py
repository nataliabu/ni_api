from app import app, db, DataTable
from flask import jsonify

@app.route("/")
def index():
    return jsonify("Hello NI!")

@app.route("/keys", methods=["GET"])
def get_all_keys_and_values():
    results = []
    for row in DataTable.query.all():
        results.append({row.key: row.value})
    return jsonify(results)

@app.route("/keys/<string:id>", methods=["GET"])
def get_value(id):
    row = DataTable.query.filter(DataTable.key == id).first()
    if row is not None:
        return jsonify(row.value)
    return jsonify("Not Found"), 404

@app.route("/keys", methods=["DELETE"])
def delete_all_values():
    db.session.query(DataTable).delete()
    db.session.commit()
    return jsonify("Deleting all database entries")

@app.route("/keys/<string:id>", methods=["DELETE"])
def delete_value(id):
    entry = DataTable.query.filter(DataTable.key == id).first()
    if entry is None:
        return jsonify("Not Found"), 404
    db.session.delete(entry)
    db.session.commit()
    return jsonify("Database entry succesfully deleted")

if __name__ == "__main__":
    app.run()
