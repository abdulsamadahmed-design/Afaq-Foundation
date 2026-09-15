import pytest

from models.user import Member
from models.event import Event
from models.volunteer import Volunteer


def create_member():
    return Member(
        1,
        "Afaq Member",
        "member@afaq.org"
    )


def create_event(capacity=50):
    return Event(
        event_id=1,
        title="Community Food Drive",
        description="Food distribution for families.",
        location="Nairobi",
        event_date="2026-10-10",
        capacity=capacity
    )


def create_volunteer(member, event):
    return Volunteer(
        volunteer_id=1,
        member=member,
        event=event,
        skills=["Communication", "Teamwork"]
    )


def test_volunteer_creation():
    member = create_member()
    event = create_event()

    volunteer = create_volunteer(member, event)

    assert volunteer.member == member
    assert volunteer.event == event
    assert volunteer.status == "registered"


def test_volunteer_registration():
    member = create_member()
    event = create_event()

    volunteer = create_volunteer(member, event)

    volunteer.register()

    assert volunteer in event.registered_volunteers
    assert event.available_slots() == 49


def test_duplicate_volunteer_registration_is_rejected():
    member = create_member()
    event = create_event()

    volunteer = create_volunteer(member, event)

    volunteer.register()

    with pytest.raises(ValueError):
        volunteer.register()


def test_event_capacity_is_enforced():
    member_one = create_member()

    member_two = Member(
        2,
        "Second Member",
        "second@afaq.org"
    )

    event = create_event(capacity=1)

    volunteer_one = Volunteer(
        1,
        member_one,
        event
    )

    volunteer_two = Volunteer(
        2,
        member_two,
        event
    )

    volunteer_one.register()

    with pytest.raises(ValueError):
        volunteer_two.register()


def test_add_skill():
    member = create_member()
    event = create_event()

    volunteer = create_volunteer(member, event)

    volunteer.add_skill("First Aid")

    assert "First Aid" in volunteer.skills


def test_duplicate_skill_is_not_added():
    member = create_member()
    event = create_event()

    volunteer = create_volunteer(member, event)

    volunteer.add_skill("Communication")

    assert volunteer.skills.count("Communication") == 1


def test_volunteer_status_can_be_updated():
    member = create_member()
    event = create_event()

    volunteer = create_volunteer(member, event)

    volunteer.update_status("confirmed")

    assert volunteer.status == "confirmed"


def test_invalid_volunteer_status_is_rejected():
    member = create_member()
    event = create_event()

    volunteer = create_volunteer(member, event)

    with pytest.raises(ValueError):
        volunteer.update_status("unknown")