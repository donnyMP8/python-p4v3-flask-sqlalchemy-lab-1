# server/app.py
#!/usr/bin/env python3
from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Earthquake

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.route("/earthquakes/<int:id>")
def get_earthquake_by_id(id):
    quake = db.session.get(Earthquake, id)

    if quake:
        return jsonify(quake.to_dict()), 200
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404


@app.route("/earthquakes/magnitude/<float:magnitude>")
def get_earthquakes_by_magnitude(magnitude):
    quakes = Earthquake.query.filter(
        Earthquake.magnitude >= magnitude
    ).all()

    return jsonify({
        "count": len(quakes),
        "quakes": [q.to_dict() for q in quakes]
    }), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
