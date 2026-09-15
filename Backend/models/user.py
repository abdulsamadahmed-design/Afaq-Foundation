class User:
    """Base class for all users in the Afaq Foundation system."""

    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.role = "user"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "role": self.role
        }

    def __str__(self):
        return f"{self.name} ({self.role})"


class Member(User):
    """Represents a regular foundation member."""

    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.role = "member"


class ProjectManager(User):
    """Represents a user responsible for managing projects."""

    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.role = "project_manager"


class Admin(User):
    """Represents an administrator."""

    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.role = "admin"


class SuperAdmin(Admin):
    """Represents the highest-level administrator."""

    def __init__(self, user_id, name, email):
        super().__init__(user_id, name, email)
        self.role = "super_admin"