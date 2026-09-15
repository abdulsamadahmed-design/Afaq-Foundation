class Project:
    """Represents a charity project managed by Afaq Foundation."""

    def __init__(
        self,
        project_id,
        title,
        description,
        category,
        location,
        target_amount,
        amount_raised=0,
        status="active"
    ):
        self.project_id = project_id
        self.title = title
        self.description = description
        self.category = category
        self.location = location
        self.target_amount = float(target_amount)
        self.amount_raised = float(amount_raised)
        self.status = status

    def add_donation(self, amount):
        """Add a donation amount to the project's total raised."""

        amount = float(amount)

        if amount <= 0:
            raise ValueError("Donation amount must be greater than 0.")

        self.amount_raised += amount

    def funding_progress(self):
        """Return the project's funding progress as a percentage."""

        if self.target_amount <= 0:
            return 0

        progress = (self.amount_raised / self.target_amount) * 100

        return round(progress, 2)

    def update_status(self, new_status):
        """Update the current status of the project."""

        allowed_statuses = ["active", "completed", "paused"]

        if new_status not in allowed_statuses:
            raise ValueError(
                "Status must be active, completed, or paused."
            )

        self.status = new_status

    def to_dict(self):
        """Convert the project object into a dictionary."""

        return {
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "location": self.location,
            "target_amount": self.target_amount,
            "amount_raised": self.amount_raised,
            "funding_progress": self.funding_progress(),
            "status": self.status
        }

    def __str__(self):
        return f"{self.title} ({self.status})"