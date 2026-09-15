import pytest

from models.event import Event


def create_event(capacity=50):
    return Event(
        event_id=1,
        title="Community Food Drive",
        description="Food distribution for families.",
        location="Nairobi",
        event_date="2026-10-10",
        capacity=capacity
    )


def test_event_creation():
    event = create_event()

    assert event.event_id == 1
    assert event.title == "Community Food Drive"
    assert event.capacity == 50
    assert event.status == "upcoming"


def test_event_starts_with_full_availability():
    event = create_event()

    assert event.available_slots() == 50


def test_event_status_can_be_updated():
    event = create_event()

    event.update_status("completed")

    assert event.status == "completed"


def test_invalid_event_status_is_rejected():
    event = create_event()

    with pytest.raises(ValueError):
        event.update_status("random")


def test_invalid_capacity_is_rejected():
    with pytest.raises(ValueError):
        create_event(capacity=0)
        