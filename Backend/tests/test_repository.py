import pytest
import database
import repository


@pytest.fixture
def test_database(tmp_path, monkeypatch):
    """
    Create a temporary database for each test.

    This prevents our tests from changing the real
    data/afaq.db database.
    """

    test_db = tmp_path / "test_afaq.db"

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_db
    )

    database.create_tables()

    return test_db


def test_create_and_get_user(test_database):
    user_id = repository.create_user(
        name="Afaq Member",
        email="member@afaq.org",
        role="member"
    )

    user = repository.get_user(user_id)

    assert user is not None
    assert user["name"] == "Afaq Member"
    assert user["email"] == "member@afaq.org"
    assert user["role"] == "member"


def test_get_user_by_email(test_database):
    repository.create_user(
        name="Afaq Admin",
        email="admin@afaq.org",
        role="admin"
    )

    user = repository.get_user_by_email(
        "admin@afaq.org"
    )

    assert user is not None
    assert user["name"] == "Afaq Admin"
    assert user["role"] == "admin"


def test_get_all_users(test_database):
    repository.create_user(
        "Member One",
        "one@afaq.org"
    )

    repository.create_user(
        "Member Two",
        "two@afaq.org"
    )

    users = repository.get_all_users()

    assert len(users) == 2


def test_update_user_role(test_database):
    user_id = repository.create_user(
        "Afaq Member",
        "member@afaq.org"
    )

    result = repository.update_user_role(
        user_id,
        "admin"
    )

    user = repository.get_user(user_id)

    assert result is True
    assert user["role"] == "admin"


def test_invalid_user_role_is_rejected(test_database):
    user_id = repository.create_user(
        "Afaq Member",
        "member@afaq.org"
    )

    with pytest.raises(ValueError):
        repository.update_user_role(
            user_id,
            "king"
        )


def test_delete_user(test_database):
    user_id = repository.create_user(
        "Delete Me",
        "delete@afaq.org"
    )

    result = repository.delete_user(user_id)

    assert result is True
    assert repository.get_user(user_id) is None


def test_create_and_get_project(test_database):
    manager_id = repository.create_user(
        "Project Manager",
        "manager@afaq.org",
        "project_manager"
    )

    project_id = repository.create_project(
        title="Education Without Barriers",
        description="Supporting access to education.",
        category="Education",
        location="Kenya",
        target_amount=100000,
        manager_id=manager_id
    )

    project = repository.get_project(project_id)

    assert project is not None
    assert project["title"] == "Education Without Barriers"
    assert project["target_amount"] == 100000.0
    assert project["amount_raised"] == 0.0
    assert project["status"] == "active"
    assert project["manager_id"] == manager_id


def test_get_all_projects(test_database):
    repository.create_project(
        "Education Project",
        "Education support.",
        "Education",
        "Nairobi",
        100000
    )

    repository.create_project(
        "Food Project",
        "Food support.",
        "Food",
        "Mombasa",
        50000
    )

    projects = repository.get_all_projects()

    assert len(projects) == 2


def test_update_project_status(test_database):
    project_id = repository.create_project(
        "Education Project",
        "Education support.",
        "Education",
        "Nairobi",
        100000
    )

    result = repository.update_project_status(
        project_id,
        "completed"
    )

    project = repository.get_project(project_id)

    assert result is True
    assert project["status"] == "completed"


def test_invalid_project_status_is_rejected(
    test_database
):
    project_id = repository.create_project(
        "Education Project",
        "Education support.",
        "Education",
        "Nairobi",
        100000
    )

    with pytest.raises(ValueError):
        repository.update_project_status(
            project_id,
            "whatever"
        )


def test_invalid_project_target_is_rejected(
    test_database
):
    with pytest.raises(ValueError):
        repository.create_project(
            "Bad Project",
            "Invalid target.",
            "Education",
            "Nairobi",
            -1000
        )


def test_delete_project(test_database):
    project_id = repository.create_project(
        "Temporary Project",
        "Testing deletion.",
        "Education",
        "Nairobi",
        10000
    )

    result = repository.delete_project(project_id)

    assert result is True
    assert repository.get_project(project_id) is None

def test_create_donation_updates_project(test_database):
    donor_id = repository.create_user(
        "Afaq Member",
        "member@afaq.org"
    )

    project_id = repository.create_project(
        "Education Project",
        "Education support.",
        "Education",
        "Nairobi",
        100000
    )

    donation_id = repository.create_donation(
        donor_id=donor_id,
        project_id=project_id,
        amount=5000,
        payment_method="M-Pesa"
    )

    donation = repository.get_donation(donation_id)
    project = repository.get_project(project_id)

    assert donation is not None
    assert donation["amount"] == 5000.0
    assert donation["donor_id"] == donor_id
    assert donation["project_id"] == project_id

    assert project["amount_raised"] == 5000.0


def test_multiple_donations_update_project(test_database):
    donor_id = repository.create_user(
        "Afaq Member",
        "member@afaq.org"
    )

    project_id = repository.create_project(
        "Food Support",
        "Supporting families.",
        "Food",
        "Nairobi",
        100000
    )

    repository.create_donation(
        donor_id,
        project_id,
        5000
    )

    repository.create_donation(
        donor_id,
        project_id,
        2500
    )

    project = repository.get_project(project_id)

    assert project["amount_raised"] == 7500.0


def test_negative_database_donation_is_rejected(
    test_database
):
    donor_id = repository.create_user(
        "Afaq Member",
        "member@afaq.org"
    )

    project_id = repository.create_project(
        "Education Project",
        "Education support.",
        "Education",
        "Nairobi",
        100000
    )

    with pytest.raises(ValueError):
        repository.create_donation(
            donor_id,
            project_id,
            -5000
        )


def test_missing_donor_is_rejected(test_database):
    project_id = repository.create_project(
        "Education Project",
        "Education support.",
        "Education",
        "Nairobi",
        100000
    )

    with pytest.raises(ValueError):
        repository.create_donation(
            donor_id=999,
            project_id=project_id,
            amount=5000
        )


def test_missing_project_is_rejected(test_database):
    donor_id = repository.create_user(
        "Afaq Member",
        "member@afaq.org"
    )

    with pytest.raises(ValueError):
        repository.create_donation(
            donor_id=donor_id,
            project_id=999,
            amount=5000
        )


def test_anonymous_donation_is_saved(test_database):
    donor_id = repository.create_user(
        "Private Donor",
        "private@afaq.org"
    )

    project_id = repository.create_project(
        "Food Support",
        "Food assistance.",
        "Food",
        "Nairobi",
        50000
    )

    donation_id = repository.create_donation(
        donor_id,
        project_id,
        2000,
        anonymous=True
    )

    donation = repository.get_donation(donation_id)

    assert donation["anonymous"] == 1

def test_create_and_get_event(test_database):
    event_id = repository.create_event(
        title="Community Food Drive",
        description="Food distribution for families.",
        location="Nairobi",
        event_date="2026-10-10",
        capacity=50
    )

    event = repository.get_event(event_id)

    assert event is not None
    assert event["title"] == "Community Food Drive"
    assert event["capacity"] == 50
    assert event["status"] == "upcoming"


def test_invalid_event_capacity_is_rejected(
    test_database
):
    with pytest.raises(ValueError):
        repository.create_event(
            "Bad Event",
            "Invalid capacity.",
            "Nairobi",
            "2026-10-10",
            0
        )


def test_update_database_event_status(
    test_database
):
    event_id = repository.create_event(
        "Community Food Drive",
        "Food distribution.",
        "Nairobi",
        "2026-10-10",
        50
    )

    repository.update_event_status(
        event_id,
        "completed"
    )

    event = repository.get_event(event_id)

    assert event["status"] == "completed"


def test_register_volunteer_in_database(
    test_database
):
    member_id = repository.create_user(
        "Afaq Member",
        "member@afaq.org"
    )

    event_id = repository.create_event(
        "Community Food Drive",
        "Food distribution.",
        "Nairobi",
        "2026-10-10",
        50
    )

    volunteer_id = repository.register_volunteer(
        member_id,
        event_id
    )

    volunteer = repository.get_volunteer(
        volunteer_id
    )

    assert volunteer is not None
    assert volunteer["member_id"] == member_id
    assert volunteer["event_id"] == event_id
    assert volunteer["status"] == "registered"


def test_duplicate_database_registration_is_rejected(
    test_database
):
    member_id = repository.create_user(
        "Afaq Member",
        "member@afaq.org"
    )

    event_id = repository.create_event(
        "Community Food Drive",
        "Food distribution.",
        "Nairobi",
        "2026-10-10",
        50
    )

    repository.register_volunteer(
        member_id,
        event_id
    )

    with pytest.raises(ValueError):
        repository.register_volunteer(
            member_id,
            event_id
        )


def test_database_event_capacity_is_enforced(
    test_database
):
    member_one = repository.create_user(
        "Member One",
        "one@afaq.org"
    )

    member_two = repository.create_user(
        "Member Two",
        "two@afaq.org"
    )

    event_id = repository.create_event(
        "Small Event",
        "Capacity test.",
        "Nairobi",
        "2026-10-10",
        1
    )

    repository.register_volunteer(
        member_one,
        event_id
    )

    with pytest.raises(ValueError):
        repository.register_volunteer(
            member_two,
            event_id
        )


def test_get_event_volunteers(
    test_database
):
    member_one = repository.create_user(
        "Member One",
        "one@afaq.org"
    )

    member_two = repository.create_user(
        "Member Two",
        "two@afaq.org"
    )

    event_id = repository.create_event(
        "Community Event",
        "Community support.",
        "Nairobi",
        "2026-10-10",
        20
    )

    repository.register_volunteer(
        member_one,
        event_id
    )

    repository.register_volunteer(
        member_two,
        event_id
    )

    volunteers = repository.get_event_volunteers(
        event_id
    )

    assert len(volunteers) == 2

    assert volunteers[0]["member_name"] == "Member One"
    assert volunteers[1]["member_name"] == "Member Two"


def test_update_database_volunteer_status(
    test_database
):
    member_id = repository.create_user(
        "Afaq Member",
        "member@afaq.org"
    )

    event_id = repository.create_event(
        "Community Event",
        "Community support.",
        "Nairobi",
        "2026-10-10",
        20
    )

    volunteer_id = repository.register_volunteer(
        member_id,
        event_id
    )

    repository.update_volunteer_status(
        volunteer_id,
        "confirmed"
    )

    volunteer = repository.get_volunteer(
        volunteer_id
    )

    assert volunteer["status"] == "confirmed"