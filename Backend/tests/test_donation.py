import pytest

from models.user import Member
from models.project import Project
from models.donation import Donation


def create_member():
    return Member(
        1,
        "Afaq Member",
        "member@afaq.org"
    )


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


def test_donation_creation():
    member = create_member()
    project = create_project()

    donation = Donation(
        donation_id=1,
        donor=member,
        project=project,
        amount=5000
    )

    assert donation.amount == 5000.0
    assert donation.donor == member
    assert donation.project == project
    assert donation.payment_method == "M-Pesa"


def test_process_donation_updates_project():
    member = create_member()
    project = create_project()

    donation = Donation(
        1,
        member,
        project,
        5000
    )

    donation.process_donation()

    assert project.amount_raised == 30000.0


def test_negative_donation_is_rejected():
    member = create_member()
    project = create_project()

    with pytest.raises(ValueError):
        Donation(
            1,
            member,
            project,
            -5000
        )


def test_anonymous_donation_hides_name():
    member = create_member()
    project = create_project()

    donation = Donation(
        donation_id=1,
        donor=member,
        project=project,
        amount=5000,
        anonymous=True
    )

    assert donation.donor_name() == "Anonymous"


def test_normal_donation_shows_name():
    member = create_member()
    project = create_project()

    donation = Donation(
        1,
        member,
        project,
        5000
    )

    assert donation.donor_name() == "Afaq Member"
    