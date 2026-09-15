from flask import Flask, jsonify, request
from flask_cors import CORS

import auth
import repository
from database import create_tables


app = Flask(__name__)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": [
                "http://localhost:5173",
                "http://127.0.0.1:5173"
            ]
        }
    }
)


def public_user(user):
    """Remove private information before sending user data."""

    if user is None:
        return None

    return {
        "id": user["id"],
        "name": user["name"],
        "email": user["email"],
        "role": user["role"]
    }


# =========================================================
# HOME
# =========================================================

@app.get("/api")
def api_home():
    return jsonify({
        "message": "Afaq Foundation API is running."
    })


# =========================================================
# AUTHENTICATION
# =========================================================

@app.post("/api/auth/register")
def register():
    data = request.get_json(silent=True) or {}

    try:
        user = auth.register_user(
            name=data.get("name", ""),
            email=data.get("email", ""),
            password=data.get("password", ""),
            role="member"
        )

        return jsonify({
            "message": "Registration successful.",
            "user": public_user(user)
        }), 201

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400


@app.post("/api/auth/login")
def login():
    data = request.get_json(silent=True) or {}

    try:
        user = auth.login_user(
            email=data.get("email", ""),
            password=data.get("password", "")
        )

        return jsonify({
            "message": "Login successful.",
            "user": public_user(user)
        })

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 401


# =========================================================
# PROJECTS
# =========================================================

@app.get("/api/projects")
def projects():
    return jsonify(repository.get_all_projects())


@app.get("/api/projects/<int:project_id>")
def project_details(project_id):
    project = repository.get_project(project_id)

    if project is None:
        return jsonify({
            "error": "Project not found."
        }), 404

    return jsonify(project)


@app.post("/api/projects")
def add_project():
    data = request.get_json(silent=True) or {}

    try:
        project_id = repository.create_project(
            title=data.get("title", ""),
            description=data.get("description", ""),
            category=data.get("category", ""),
            location=data.get("location", ""),
            target_amount=data.get("target_amount", 0),
            manager_id=data.get("manager_id")
        )

        project = repository.get_project(project_id)

        return jsonify(project), 201

    except (ValueError, TypeError) as error:
        return jsonify({
            "error": str(error)
        }), 400


@app.patch("/api/projects/<int:project_id>/status")
def change_project_status(project_id):
    data = request.get_json(silent=True) or {}

    try:
        updated = repository.update_project_status(
            project_id,
            data.get("status", "")
        )

        if not updated:
            return jsonify({
                "error": "Project not found."
            }), 404

        return jsonify(
            repository.get_project(project_id)
        )

    except ValueError as error:
        return jsonify({
            "error": str(error)
        }), 400


# =========================================================
# DONATIONS
# =========================================================

@app.post("/api/donations")
def add_donation():
    data = request.get_json(silent=True) or {}

    try:
        donation_id = repository.create_donation(
            donor_id=data.get("donor_id"),
            project_id=data.get("project_id"),
            amount=data.get("amount", 0),
            payment_method=data.get(
                "payment_method",
                "M-Pesa"
            ),
            anonymous=data.get("anonymous", False)
        )

        donation = repository.get_donation(
            donation_id
        )

        return jsonify(donation), 201

    except (ValueError, TypeError) as error:
        return jsonify({
            "error": str(error)
        }), 400


@app.get("/api/projects/<int:project_id>/donations")
def project_donations(project_id):
    project = repository.get_project(project_id)

    if project is None:
        return jsonify({
            "error": "Project not found."
        }), 404

    return jsonify(
        repository.get_project_donations(project_id)
    )


# =========================================================
# EVENTS
# =========================================================

@app.get("/api/events")
def events():
    return jsonify(repository.get_all_events())


@app.post("/api/events")
def add_event():
    data = request.get_json(silent=True) or {}

    try:
        event_id = repository.create_event(
            title=data.get("title", ""),
            description=data.get(
                "description",
                ""
            ),
            location=data.get("location", ""),
            event_date=data.get("event_date", ""),
            capacity=data.get("capacity", 0)
        )

        return jsonify(
            repository.get_event(event_id)
        ), 201

    except (ValueError, TypeError) as error:
        return jsonify({
            "error": str(error)
        }), 400


# =========================================================
# VOLUNTEERS
# =========================================================

@app.post("/api/events/<int:event_id>/volunteers")
def add_volunteer(event_id):
    data = request.get_json(silent=True) or {}

    try:
        volunteer_id = repository.register_volunteer(
            member_id=data.get("member_id"),
            event_id=event_id
        )

        return jsonify(
            repository.get_volunteer(volunteer_id)
        ), 201

    except (ValueError, TypeError) as error:
        return jsonify({
            "error": str(error)
        }), 400


@app.get("/api/events/<int:event_id>/volunteers")
def event_volunteers(event_id):
    event = repository.get_event(event_id)

    if event is None:
        return jsonify({
            "error": "Event not found."
        }), 404

    return jsonify(
        repository.get_event_volunteers(event_id)
    )


# =========================================================
# START APPLICATION
# =========================================================

if __name__ == "__main__":
    create_tables()

    app.run(
        debug=True,
        port=5000
    )
    