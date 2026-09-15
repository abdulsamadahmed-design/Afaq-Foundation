import bcrypt

from repository import (
    create_user,
    get_user_by_email
)


def hash_password(password):
    """Hash a password securely using bcrypt."""

    if not isinstance(password, str):
        raise ValueError("Password must be a string.")

    if len(password) < 6:
        raise ValueError(
            "Password must contain at least 6 characters."
        )

    password_bytes = password.encode("utf-8")

    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    return hashed_password.decode("utf-8")


def verify_password(password, password_hash):
    """Check whether a password matches its stored hash."""

    if not password or not password_hash:
        return False

    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8")
        )

    except (ValueError, TypeError):
        return False


def register_user(
    name,
    email,
    password,
    role="member"
):
    """Register a new Afaq Foundation user."""

    name = name.strip()
    email = email.strip().lower()

    if not name:
        raise ValueError("Name is required.")

    if not email:
        raise ValueError("Email is required.")

    if "@" not in email:
        raise ValueError("Invalid email address.")

    existing_user = get_user_by_email(email)

    if existing_user:
        raise ValueError(
            "A user with this email already exists."
        )

    allowed_roles = [
        "member",
        "project_manager",
        "admin",
        "super_admin"
    ]

    if role not in allowed_roles:
        raise ValueError("Invalid user role.")

    password_hash = hash_password(password)

    user_id = create_user(
        name=name,
        email=email,
        role=role,
        password_hash=password_hash
    )

    return get_user_by_email(email)


def login_user(email, password):
    """Authenticate a user using email and password."""

    email = email.strip().lower()

    user = get_user_by_email(email)

    if user is None:
        raise ValueError("Invalid email or password.")

    if not verify_password(
        password,
        user["password_hash"]
    ):
        raise ValueError("Invalid email or password.")

    return user
