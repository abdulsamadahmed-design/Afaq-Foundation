from database import create_tables, get_connection
from repository import create_project


def project_exists(title):
    """Check whether a project has already been seeded."""
    connection = get_connection()

    project = connection.execute(
        """
        SELECT id
        FROM projects
        WHERE title = ?
        """,
        (title,)
    ).fetchone()

    connection.close()

    return project is not None


def seed_projects():
    """Add the initial Afaq Foundation projects."""

    projects = [
        {
            "title": "Education Without Barriers",
            "summary": (
                "Supporting students with access to education, "
                "learning materials, and essential school resources."
            ),
            "description": (
                "Education Without Barriers helps students from "
                "underserved communities continue their education "
                "by providing school supplies, learning resources, "
                "and educational support."
            ),
            "category": "Education",
            "location": "Nairobi",
            "target_amount": 500000,
            "amount_raised": 360000,
            "beneficiaries": 240,
            "icon": "🎓",
            "status": "active",
            "goals": [
                "Provide essential learning materials to students.",
                "Support students from underserved communities.",
                "Improve access to quality education."
            ],
            "updates": [
                [
                    "Learning materials distributed",
                    "School supplies have been delivered to students."
                ],
                [
                    "Community outreach completed",
                    "Families and schools were engaged in the program."
                ]
            ]
        },
        {
            "title": "Ramadan Food Support",
            "summary": (
                "Providing food packages to families during "
                "the holy month of Ramadan."
            ),
            "description": (
                "Ramadan Food Support provides essential food "
                "packages to vulnerable families, helping households "
                "meet their daily needs throughout Ramadan."
            ),
            "category": "Community Care",
            "location": "Nairobi",
            "target_amount": 500000,
            "amount_raised": 420000,
            "beneficiaries": 380,
            "icon": "🥫",
            "status": "active",
            "goals": [
                "Distribute food packages to vulnerable families.",
                "Support households throughout Ramadan.",
                "Strengthen community support and care."
            ],
            "updates": [
                [
                    "Food packages prepared",
                    "The first group of family food packages is ready."
                ],
                [
                    "Distribution underway",
                    "Volunteers have started distributing packages."
                ]
            ]
        },
        {
            "title": "Youth Skills Lab",
            "summary": (
                "Helping young people develop practical digital "
                "and career skills."
            ),
            "description": (
                "Youth Skills Lab equips young people with practical "
                "digital, technology, and career skills to help them "
                "prepare for education and employment opportunities."
            ),
            "category": "Youth",
            "location": "Nairobi",
            "target_amount": 500000,
            "amount_raised": 280000,
            "beneficiaries": 120,
            "icon": "💻",
            "status": "active",
            "goals": [
                "Provide practical digital skills training.",
                "Improve career readiness among young people.",
                "Create opportunities for mentorship and growth."
            ],
            "updates": [
                [
                    "Training sessions started",
                    "The first group has begun digital skills training."
                ],
                [
                    "Mentorship introduced",
                    "Participants are receiving career guidance."
                ]
            ]
        },
        {
            "title": "Community Water Access",
            "summary": (
                "Improving access to safe and reliable water "
                "for communities."
            ),
            "description": (
                "Community Water Access aims to improve access to "
                "clean and reliable water by supporting sustainable "
                "community water infrastructure."
            ),
            "category": "Development",
            "location": "Kenya",
            "target_amount": 750000,
            "amount_raised": 0,
            "beneficiaries": 600,
            "icon": "💧",
            "status": "upcoming",
            "goals": [
                "Improve access to safe water.",
                "Support sustainable water infrastructure.",
                "Serve approximately 600 beneficiaries."
            ],
            "updates": [
                [
                    "Project preparation",
                    "Planning and community assessment are underway."
                ]
            ]
        },
        {
            "title": "School Kit Drive",
            "summary": (
                "Providing complete school kits to students "
                "who need them most."
            ),
            "description": (
                "School Kit Drive provided students with essential "
                "school supplies including books, stationery, "
                "and other learning materials."
            ),
            "category": "Education",
            "location": "Nairobi",
            "target_amount": 200000,
            "amount_raised": 200000,
            "beneficiaries": 160,
            "icon": "📚",
            "status": "completed",
            "goals": [
                "Provide complete school kits to students.",
                "Reduce barriers caused by lack of school supplies.",
                "Support 160 students with learning materials."
            ],
            "updates": [
                [
                    "Fundraising completed",
                    "The project reached its full funding target."
                ],
                [
                    "School kits distributed",
                    "All planned school kits were successfully distributed."
                ]
            ]
        }
    ]

    added = 0
    skipped = 0

    for project in projects:
        if project_exists(project["title"]):
            print(f"SKIPPED: {project['title']}")
            skipped += 1
            continue

        create_project(**project)

        print(f"ADDED: {project['title']}")
        added += 1

    print()
    print("Afaq Foundation seed complete.")
    print(f"Projects added: {added}")
    print(f"Projects skipped: {skipped}")


if __name__ == "__main__":
    create_tables()
    seed_projects()