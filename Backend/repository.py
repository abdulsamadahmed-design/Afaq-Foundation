import json  

from database import get_connection


# =========================================================
# USERS
# =========================================================

def create_user(name, email, role="member", password_hash=None):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (name, email, password_hash, role)
        VALUES (?, ?, ?, ?)
        """,
        (name, email, password_hash, role)
    )

    connection.commit()
    user_id = cursor.lastrowid
    connection.close()

    return user_id


def get_user(user_id):
    connection = get_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    ).fetchone()

    connection.close()

    return dict(user) if user else None


def get_user_by_email(email):
    connection = get_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    ).fetchone()

    connection.close()

    return dict(user) if user else None


def get_all_users():
    connection = get_connection()

    users = connection.execute(
        "SELECT * FROM users"
    ).fetchall()

    connection.close()

    return [dict(user) for user in users]


def update_user_role(user_id, new_role):
    allowed_roles = [
        "member",
        "project_manager",
        "admin",
        "super_admin"
    ]

    if new_role not in allowed_roles:
        raise ValueError("Invalid user role.")

    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE users
        SET role = ?
        WHERE id = ?
        """,
        (new_role, user_id)
    )

    connection.commit()
    updated = cursor.rowcount > 0
    connection.close()

    return updated


def delete_user(user_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )

    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()

    return deleted


# =========================================================
# PROJECTS
# =========================================================

def serialize_project(project):
    """Convert a project database row into API-friendly data."""

    if project is None:
        return None

    project = dict(project)

    project["goals"] = json.loads(
        project.get("goals") or "[]"
    )

    project["updates"] = json.loads(
        project.get("updates") or "[]"
    )

    return project

def create_project(
    title,
    description,
    category,
    location,
    target_amount,
    manager_id=None,
    summary="",
    amount_raised=0,
    beneficiaries=0,
    icon="🤝",
    goals=None,
    updates=None,
    status="active"
):
    target_amount = float(target_amount)
    amount_raised = float(amount_raised)
    beneficiaries = int(beneficiaries)

    if target_amount <= 0:
        raise ValueError(
            "Target amount must be greater than 0."
        )

    if amount_raised < 0:
        raise ValueError(
            "Amount raised cannot be negative."
        )

    if beneficiaries < 0:
        raise ValueError(
            "Beneficiaries cannot be negative."
        )

    allowed_statuses = [
        "active",
        "completed",
        "paused",
        "upcoming"
    ]

    if status not in allowed_statuses:
        raise ValueError("Invalid project status.")

    goals = goals if goals is not None else []
    updates = updates if updates is not None else []

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO projects (
            title,
            summary,
            description,
            category,
            location,
            target_amount,
            amount_raised,
            beneficiaries,
            icon,
            goals,
            updates,
            status,
            manager_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            summary,
            description,
            category,
            location,
            target_amount,
            amount_raised,
            beneficiaries,
            icon,
            json.dumps(goals),
            json.dumps(updates),
            status,
            manager_id
        )
    )

    connection.commit()
    project_id = cursor.lastrowid
    connection.close()

    return project_id

def get_project(project_id):
    connection = get_connection()

    project = connection.execute(
        """
        SELECT *
        FROM projects
        WHERE id = ?
        """,
        (project_id,)
    ).fetchone()

    connection.close()

    return serialize_project(project)


def get_all_projects():
    connection = get_connection()

    projects = connection.execute(
        """
        SELECT *
        FROM projects
        ORDER BY id
        """
    ).fetchall()

    connection.close()

    return [
        serialize_project(project)
        for project in projects
    ]

def update_project_status(project_id, new_status):
    allowed_statuses = [
        "active",
        "completed",
        "paused"
        "upcoming"
    ]

    if new_status not in allowed_statuses:
        raise ValueError("Invalid project status.")

    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE projects
        SET status = ?
        WHERE id = ?
        """,
        (new_status, project_id)
    )

    connection.commit()
    updated = cursor.rowcount > 0
    connection.close()

    return updated


def delete_project(project_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM projects WHERE id = ?",
        (project_id,)
    )

    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()

    return deleted
# =========================================================
# DONATIONS
# =========================================================

def create_donation(
    donor_id,
    project_id,
    amount,
    payment_method="M-Pesa",
    anonymous=False
):
    """
    Save a donation and update the project's amount raised.

    Both operations happen in the same database transaction.
    """

    amount = float(amount)

    if amount <= 0:
        raise ValueError("Donation amount must be greater than 0.")

    connection = get_connection()

    try:
        # Make sure donor exists
        donor = connection.execute(
            "SELECT id FROM users WHERE id = ?",
            (donor_id,)
        ).fetchone()

        if donor is None:
            raise ValueError("Donor does not exist.")

        # Make sure project exists
        project = connection.execute(
            "SELECT id FROM projects WHERE id = ?",
            (project_id,)
        ).fetchone()

        if project is None:
            raise ValueError("Project does not exist.")

        cursor = connection.cursor()

        # Save donation
        cursor.execute(
            """
            INSERT INTO donations (
                donor_id,
                project_id,
                amount,
                payment_method,
                anonymous
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                donor_id,
                project_id,
                amount,
                payment_method,
                int(anonymous)
            )
        )

        donation_id = cursor.lastrowid

        # Update project funding
        cursor.execute(
            """
            UPDATE projects
            SET amount_raised = amount_raised + ?
            WHERE id = ?
            """,
            (amount, project_id)
        )

        connection.commit()

        return donation_id

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_donation(donation_id):
    connection = get_connection()

    donation = connection.execute(
        """
        SELECT *
        FROM donations
        WHERE id = ?
        """,
        (donation_id,)
    ).fetchone()

    connection.close()

    return dict(donation) if donation else None


def get_all_donations():
    connection = get_connection()

    donations = connection.execute(
        """
        SELECT *
        FROM donations
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return [dict(donation) for donation in donations]


def get_project_donations(project_id):
    connection = get_connection()

    donations = connection.execute(
        """
        SELECT *
        FROM donations
        WHERE project_id = ?
        ORDER BY id DESC
        """,
        (project_id,)
    ).fetchall()

    connection.close()

    return [dict(donation) for donation in donations]


def get_user_donations(donor_id):
    connection = get_connection()

    donations = connection.execute(
        """
        SELECT *
        FROM donations
        WHERE donor_id = ?
        ORDER BY id DESC
        """,
        (donor_id,)
    ).fetchall()

    connection.close()

    return [dict(donation) for donation in donations]

# =========================================================
# EVENTS
# =========================================================

def create_event(
    title,
    description,
    location,
    event_date,
    capacity,
    status="upcoming"
):
    capacity = int(capacity)

    if capacity <= 0:
        raise ValueError("Event capacity must be greater than 0.")

    allowed_statuses = [
        "upcoming",
        "ongoing",
        "completed",
        "cancelled"
    ]

    if status not in allowed_statuses:
        raise ValueError("Invalid event status.")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO events (
            title,
            description,
            location,
            event_date,
            capacity,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            location,
            event_date,
            capacity,
            status
        )
    )

    connection.commit()

    event_id = cursor.lastrowid

    connection.close()

    return event_id


def get_event(event_id):
    connection = get_connection()

    event = connection.execute(
        """
        SELECT *
        FROM events
        WHERE id = ?
        """,
        (event_id,)
    ).fetchone()

    connection.close()

    return dict(event) if event else None


def get_all_events():
    connection = get_connection()

    events = connection.execute(
        """
        SELECT *
        FROM events
        ORDER BY event_date
        """
    ).fetchall()

    connection.close()

    return [dict(event) for event in events]


def update_event_status(event_id, new_status):
    allowed_statuses = [
        "upcoming",
        "ongoing",
        "completed",
        "cancelled"
    ]

    if new_status not in allowed_statuses:
        raise ValueError("Invalid event status.")

    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE events
        SET status = ?
        WHERE id = ?
        """,
        (new_status, event_id)
    )

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated


def delete_event(event_id):
    connection = get_connection()

    cursor = connection.execute(
        """
        DELETE FROM events
        WHERE id = ?
        """,
        (event_id,)
    )

    connection.commit()

    deleted = cursor.rowcount > 0

    connection.close()

    return deleted


# =========================================================
# VOLUNTEERS
# =========================================================

def register_volunteer(
    member_id,
    event_id,
    status="registered"
):
    allowed_statuses = [
        "registered",
        "confirmed",
        "completed",
        "cancelled"
    ]

    if status not in allowed_statuses:
        raise ValueError("Invalid volunteer status.")

    connection = get_connection()

    try:
        # Check that the member exists
        member = connection.execute(
            """
            SELECT id
            FROM users
            WHERE id = ?
            """,
            (member_id,)
        ).fetchone()

        if member is None:
            raise ValueError("Member does not exist.")

        # Check that the event exists
        event = connection.execute(
            """
            SELECT *
            FROM events
            WHERE id = ?
            """,
            (event_id,)
        ).fetchone()

        if event is None:
            raise ValueError("Event does not exist.")

        # Count active registrations
        registered_count = connection.execute(
            """
            SELECT COUNT(*) AS total
            FROM volunteers
            WHERE event_id = ?
            AND status != 'cancelled'
            """,
            (event_id,)
        ).fetchone()["total"]

        if registered_count >= event["capacity"]:
            raise ValueError(
                "Event has reached maximum capacity."
            )

        # Check duplicate registration
        existing = connection.execute(
            """
            SELECT id
            FROM volunteers
            WHERE member_id = ?
            AND event_id = ?
            """,
            (member_id, event_id)
        ).fetchone()

        if existing is not None:
            raise ValueError(
                "Member is already registered for this event."
            )

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO volunteers (
                member_id,
                event_id,
                status
            )
            VALUES (?, ?, ?)
            """,
            (
                member_id,
                event_id,
                status
            )
        )

        connection.commit()

        return cursor.lastrowid

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()


def get_volunteer(volunteer_id):
    connection = get_connection()

    volunteer = connection.execute(
        """
        SELECT *
        FROM volunteers
        WHERE id = ?
        """,
        (volunteer_id,)
    ).fetchone()

    connection.close()

    return dict(volunteer) if volunteer else None


def get_event_volunteers(event_id):
    connection = get_connection()

    volunteers = connection.execute(
        """
        SELECT
            volunteers.id,
            volunteers.member_id,
            volunteers.event_id,
            volunteers.status,
            users.name AS member_name,
            users.email AS member_email
        FROM volunteers
        JOIN users
            ON volunteers.member_id = users.id
        WHERE volunteers.event_id = ?
        ORDER BY volunteers.id
        """,
        (event_id,)
    ).fetchall()

    connection.close()

    return [dict(volunteer) for volunteer in volunteers]


def update_volunteer_status(
    volunteer_id,
    new_status
):
    allowed_statuses = [
        "registered",
        "confirmed",
        "completed",
        "cancelled"
    ]

    if new_status not in allowed_statuses:
        raise ValueError("Invalid volunteer status.")

    connection = get_connection()

    cursor = connection.execute(
        """
        UPDATE volunteers
        SET status = ?
        WHERE id = ?
        """,
        (new_status, volunteer_id)
    )

    connection.commit()

    updated = cursor.rowcount > 0

    connection.close()

    return updated
