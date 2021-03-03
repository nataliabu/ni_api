from app import app, db, DataTable
from flask import jsonify, request


@app.route("/")
def index():
    return jsonify("Hello NI!")


@app.route("/keys", methods=["GET"])
def get_all_and_filter():
    results = []

    # Support wildcard
    if "filter" in request.args:
        filt = str(request.args["filter"])
        filtered_keys = DataTable.key.like("%"+filt+"%")
        for row in DataTable.query.filter(filtered_keys).all():
            results.append({row.key: row.value})

    # Get all keys and values
    else:
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
    return jsonify("Deleting database entry")


@app.route("/keys", methods=["PUT"])
def put_value():
    entry_request = request.get_json()
    if entry_request is None:
        return jsonify("json expected as Content-Type"), 400
    elif type(entry_request) != dict:
        return jsonify("Expected a dictionary with a string as a key and "
                       "a string as its value"), 400
    for request_key, request_value in entry_request.items():
        existent_key = DataTable.query.filter(
                DataTable.key == request_key
                ).first()
        if existent_key is not None:
            existent_key.value = request_value
        else:
            new = DataTable(key=request_key, value=request_value)
            db.session.add(new)
    try:
        db.session.commit()
        return jsonify("Setting value")
    except Exception:
        db.session.rollback()
        return jsonify("Expected a dictionary with a string as a key and "
                       "a string as its value"), 400


if __name__ == "__main__":
    app.run()
