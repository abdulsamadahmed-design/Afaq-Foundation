from models.user import Member, ProjectManager, Admin, SuperAdmin
from models.project import Project
from models.donation import Donation
from models.event import Event
from models.volunteer import Volunteer


def main():

    # =====================================
    # USERS
    # =====================================

    member = Member(
        1,
        "Afaq Member",
        "member@afaq.org"
    )

    manager = ProjectManager(
        2,
        "Project Manager",
        "manager@afaq.org"
    )

    admin = Admin(
        3,
        "Afaq Admin",
        "admin@afaq.org"
    )

    super_admin = SuperAdmin(
        4,
        "Super Admin",
        "superadmin@afaq.org"
    )

    print("=== USERS ===")
    print(member)
    print(manager)
    print(admin)
    print(super_admin)

    # =====================================
    # PROJECT
    # =====================================

    project = Project(
        project_id=1,
        title="Education Without Barriers",
        description="Supporting access to education for children.",
        category="Education",
        location="Kenya",
        target_amount=100000,
        amount_raised=25000
    )

    print("\n=== PROJECT ===")
    print(project)

    print("\nBefore donation:")
    print(f"Amount raised: KSh {project.amount_raised}")
    print(f"Progress: {project.funding_progress()}%")

    # =====================================
    # DONATION
    # =====================================

    donation = Donation(
        donation_id=1,
        donor=member,
        project=project,
        amount=5000,
        payment_method="M-Pesa"
    )

    donation.process_donation()

    print("\n=== DONATION ===")
    print(donation)
    print(donation.to_dict())

    print("\nAfter donation:")
    print(f"Amount raised: KSh {project.amount_raised}")
    print(f"Progress: {project.funding_progress()}%")

    # =====================================
    # EVENT
    # =====================================

    event = Event(
        event_id=1,
        title="Community Food Drive",
        description="Food distribution for families in need.",
        location="Nairobi",
        event_date="2026-10-10",
        capacity=50
    )

    print("\n=== EVENT ===")
    print(event)

    print(
        f"Available volunteer slots: "
        f"{event.available_slots()}"
    )

    # =====================================
    # VOLUNTEER
    # =====================================

    volunteer = Volunteer(
        volunteer_id=1,
        member=member,
        event=event,
        skills=["Communication", "Teamwork"]
    )

    volunteer.register()

    print("\n=== VOLUNTEER ===")
    print(volunteer)
    print(volunteer.to_dict())

    print("\nAfter volunteer registration:")
    print(
        f"Registered volunteers: "
        f"{len(event.registered_volunteers)}"
    )
    print(
        f"Available slots: "
        f"{event.available_slots()}"
    )


if __name__ == "__main__":
    main()
    