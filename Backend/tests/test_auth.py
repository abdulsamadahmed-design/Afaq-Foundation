import pytest

import auth
import database
import repository


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    test_db = tmp_path / "test_auth.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_db
    )

    database.create_tables()

    return test_db


def test_password_is_hashed():
    password = "secret123"

    password_hash = auth.hash_password(password)

    assert password_hash != password
    assert password_hash.startswith("$2")


def test_correct_password_is_verified():
    password = "secret123"

    password_hash = auth.hash_password(password)

    assert auth.verify_password(
        password,
        password_hash
    ) is True


def test_wrong_password_is_rejected():
    password_hash = auth.hash_password(
        "secret123"
    )

    assert auth.verify_password(
        "wrongpassword",
        password_hash
    ) is False


def test_short_password_is_rejected():
    with pytest.raises(ValueError):
        auth.hash_password("123")


def test_register_user(test_database):
    user = auth.register_user(
        name="Afaq Member",
        email="member@afaq.org",
        password="secret123"
    )

    assert user["name"] == "Afaq Member"
    assert user["email"] == "member@afaq.org"
    assert user["role"] == "member"

    assert user["password_hash"] != "secret123"


def test_registered_password_is_hashed(
    test_database
):
    auth.register_user(
        name="Afaq Member",
        email="member@afaq.org",
        password="secret123"
    )

    user = repository.get_user_by_email(
        "member@afaq.org"
    )

    assert user["password_hash"] is not None

    assert auth.verify_password(
        "secret123",
        user["password_hash"]
    )


def test_duplicate_email_is_rejected(
    test_database
):
    auth.register_user(
        "Member One",
        "member@afaq.org",
        "secret123"
    )

    with pytest.raises(ValueError):
        auth.register_user(
            "Member Two",
            "member@afaq.org",
            "another123"
        )


def test_invalid_email_is_rejected(
    test_database
):
    with pytest.raises(ValueError):
        auth.register_user(
            "Afaq Member",
            "not-an-email",
            "secret123"
        )


def test_login_with_correct_password(
    test_database
):
    auth.register_user(
        "Afaq Member",
        "member@afaq.org",
        "secret123"
    )

    user = auth.login_user(
        "member@afaq.org",
        "secret123"
    )

    assert user["email"] == "member@afaq.org"


def test_login_with_wrong_password(
    test_database
):
    auth.register_user(
        "Afaq Member",
        "member@afaq.org",
        "secret123"
    )

    with pytest.raises(ValueError):
        auth.login_user(
            "member@afaq.org",
            "wrongpassword"
        )


def test_login_with_unknown_email(
    test_database
):
    with pytest.raises(ValueError):
        auth.login_user(
            "unknown@afaq.org",
            "secret123"
        )


def test_email_is_normalized(
    test_database
):
    auth.register_user(
        "Afaq Member",
        "MEMBER@AFAQ.ORG",
        "secret123"
    )

    user = repository.get_user_by_email(
        "member@afaq.org"
    )

    assert user is not None
    assert user["email"] == "member@afaq.org"
    