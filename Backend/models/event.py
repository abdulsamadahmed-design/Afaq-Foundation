class Event:
    """Represents an event organized by Afaq Foundation."""

    def __init__(
        self,
        event_id,
        title,
        description,
        location,
        event_date,
        capacity,
        status="upcoming"
    ):
        self.event_id = event_id
        self.title = title
        self.description = description
        self.location = location
        self.event_date = event_date
        self.capacity = int(capacity)
        self.status = status
        self.registered_volunteers = []

        if self.capacity <= 0:
            raise ValueError("Event capacity must be greater than 0.")

    def register_volunteer(self, volunteer):
        """Register a volunteer for the event."""

        if len(self.registered_volunteers) >= self.capacity:
            raise ValueError("Event has reached maximum capacity.")

        if volunteer in self.registered_volunteers:
            raise ValueError("Volunteer is already registered.")

        self.registered_volunteers.append(volunteer)

    def available_slots(self):
        """Return the number of remaining volunteer slots."""

        return self.capacity - len(self.registered_volunteers)

    def update_status(self, new_status):
        """Update the event status."""

        allowed_statuses = [
            "upcoming",
            "ongoing",
            "completed",
            "cancelled"
        ]

        if new_status not in allowed_statuses:
            raise ValueError("Invalid event status.")

        self.status = new_status

    def to_dict(self):
        """Convert the event object into a dictionary."""

        return {
            "event_id": self.event_id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "event_date": self.event_date,
            "capacity": self.capacity,
            "registered_volunteers": len(
                self.registered_volunteers
            ),
            "available_slots": self.available_slots(),
            "status": self.status
        }

    def __str__(self):
        return f"{self.title} - {self.event_date} ({self.status})"