from enum import Enum
from typing import List, Optional

class Role(str, Enum):
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"
    SYSTEM = "system"

class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    PUBLISH = "publish"

# Simple role-permission mapping
ROLE_PERMISSIONS = {
    Role.ADMIN: [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.PUBLISH],
    Role.EDITOR: [Permission.READ, Permission.WRITE, Permission.PUBLISH],
    Role.VIEWER: [Permission.READ],
    Role.SYSTEM: [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.PUBLISH],
}

def check_access(user_roles: List[Role], required_permission: Permission) -> bool:
    """
    Check if any of the user's roles have the required permission.
    """
    for role in user_roles:
        if required_permission in ROLE_PERMISSIONS.get(role, []):
            return True
    return False
