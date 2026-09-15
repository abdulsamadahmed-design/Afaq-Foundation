from models.user import User, Member, ProjectManager, Admin, SuperAdmin


def test_user_creation():
    user = User(1, "Test User", "test@afaq.org")

    assert user.user_id == 1
    assert user.name == "Test User"
    assert user.email == "test@afaq.org"
    assert user.role == "user"


def test_member_inherits_from_user():
    member = Member(2, "Afaq Member", "member@afaq.org")

    assert isinstance(member, User)
    assert member.role == "member"


def test_project_manager_inherits_from_user():
    manager = ProjectManager(
        3,
        "Project Manager",
        "manager@afaq.org"
    )

    assert isinstance(manager, User)
    assert manager.role == "project_manager"


def test_admin_inherits_from_user():
    admin = Admin(4, "Afaq Admin", "admin@afaq.org")

    assert isinstance(admin, User)
    assert admin.role == "admin"


def test_super_admin_inherits_from_admin():
    super_admin = SuperAdmin(
        5,
        "Super Admin",
        "superadmin@afaq.org"
    )

    assert isinstance(super_admin, Admin)
    assert isinstance(super_admin, User)
    assert super_admin.role == "super_admin"


def test_user_to_dict():
    member = Member(1, "Afaq Member", "member@afaq.org")

    data = member.to_dict()

    assert data["user_id"] == 1
    assert data["name"] == "Afaq Member"
    assert data["email"] == "member@afaq.org"
    assert data["role"] == "member"
    