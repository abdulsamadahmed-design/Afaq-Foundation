class Donation:
    """Represents a donation made by a donor to an Afaq Foundation project."""

    def __init__(
        self,
        donation_id,
        donor,
        project,
        amount,
        payment_method="M-Pesa",
        anonymous=False
    ):
        self.donation_id = donation_id
        self.donor = donor
        self.project = project
        self.payment_method = payment_method
        self.anonymous = anonymous

        self.amount = float(amount)

        if self.amount <= 0:
            raise ValueError("Donation amount must be greater than 0.")

    def process_donation(self):
        """Add the donation amount to the selected project."""

        self.project.add_donation(self.amount)

    def donor_name(self):
        """Hide the donor's name when the donation is anonymous."""

        if self.anonymous:
            return "Anonymous"

        return self.donor.name

    def to_dict(self):
        """Convert the donation object into a dictionary."""

        return {
            "donation_id": self.donation_id,
            "donor_id": self.donor.user_id,
            "donor_name": self.donor_name(),
            "project_id": self.project.project_id,
            "project_title": self.project.title,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "anonymous": self.anonymous
        }

    def __str__(self):
        return (
            f"Donation #{self.donation_id}: "
            f"{self.donor_name()} donated "
            f"KSh {self.amount:.2f} to {self.project.title}"
        )