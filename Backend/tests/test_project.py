import pytest

from models.project import Project


def create_project():
    return Project(
        project_id=1,
        title="Education Without Barriers",
        description="Supporting access to education.",
        category="Education",
        location="Kenya",
        target_amount=100000,
        amount_raised=25000
    )


def test_project_creation():
    project = create_project()

    assert project.project_id == 1
    assert project.title == "Education Without Barriers"
    assert project.target_amount == 100000.0
    assert project.amount_raised == 25000.0
    assert project.status == "active"


def test_project_add_donation():
    project = create_project()

    project.add_donation(5000)

    assert project.amount_raised == 30000.0


def test_project_funding_progress():
    project = create_project()

    assert project.funding_progress() == 25.0


def test_negative_donation_is_rejected():
    project = create_project()

    with pytest.raises(ValueError):
        project.add_donation(-5000)


def test_zero_donation_is_rejected():
    project = create_project()

    with pytest.raises(ValueError):
        project.add_donation(0)


def test_project_status_can_be_updated():
    project = create_project()

    project.update_status("completed")

    assert project.status == "completed"


def test_invalid_project_status_is_rejected():
    project = create_project()

    with pytest.raises(ValueError):
        project.update_status("unknown")
        