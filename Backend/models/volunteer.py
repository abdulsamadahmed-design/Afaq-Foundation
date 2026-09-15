class Volunteer:
    """Represents a volunteer registration for an Afaq Foundation event."""

    def __init__(
        self,
        volunteer_id,
        member,
        event,
        skills=None,
        status="registered"
    ):
        self.volunteer_id = volunteer_id
        self.member = member
        self.event = event
        self.skills = skills if skills else []
        self.status = status

    def register(self):
        """Register this volunteer with the selected event."""

        self.event.register_volunteer(self)

    def add_skill(self, skill):
        """Add a skill to the volunteer's skill list."""

        if skill not in self.skills:
            self.skills.append(skill)

    def update_status(self, new_status):
        """Update the volunteer registration status."""

        allowed_statuses = [
            "registered",
            "confirmed",
            "completed",
            "cancelled"
        ]

        if new_status not in allowed_statuses:
            raise ValueError("Invalid volunteer status.")

        self.status = new_status

    def to_dict(self):
        """Convert the volunteer object into a dictionary."""

        return {
            "volunteer_id": self.volunteer_id,
            "member_id": self.member.user_id,
            "member_name": self.member.name,
            "event_id": self.event.event_id,
            "event_title": self.event.title,
            "skills": self.skills,
            "status": self.status
        }

    def __str__(self):
        return (
            f"{self.member.name} volunteering for "
            f"{self.event.title} ({self.status})"
        )