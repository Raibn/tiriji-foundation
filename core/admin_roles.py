from django.contrib.auth.models import Group

ADMIN_ROLE_CHOICES = [
    ('sys_admin', 'System Admin'),
    ('director', 'Director'),
    ('admin', 'Admin'),
    ('secretary', 'Secretary'),
]

ADMIN_GROUP_NAMES = [
    'sys_admin',
    'director',
    'admin',
    'secretary',
]

# Only sys_admin (and superusers) bypass role checks — all other groups are
# restricted to the specific endpoints their role is allowed on.
FULL_ACCESS_GROUPS = {'sys_admin'}


def is_admin_identity(user):
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.is_staff:
        return True
    return user.groups.filter(name__in=ADMIN_GROUP_NAMES).exists()


def user_has_admin_access(user):
    return is_admin_identity(user)


def user_has_any_admin_role(user, allowed_groups):
    if not user.is_authenticated:
        return False
    if user.is_superuser or user.groups.filter(name__in=FULL_ACCESS_GROUPS).exists():
        return True
    return user.groups.filter(name__in=allowed_groups).exists()


def ensure_admin_groups():
    for group_name in ADMIN_GROUP_NAMES:
        Group.objects.get_or_create(name=group_name)


def assign_admin_role(user, role_name):
    ensure_admin_groups()
    user.groups.remove(*Group.objects.filter(name__in=ADMIN_GROUP_NAMES))
    if role_name:
        group, _ = Group.objects.get_or_create(name=role_name)
        user.groups.add(group)


def get_admin_role_label(user):
    if user.is_superuser:
        return 'Superuser'
    role_lookup = dict(ADMIN_ROLE_CHOICES)
    role = user.groups.filter(name__in=[choice[0] for choice in ADMIN_ROLE_CHOICES]).first()
    if role:
        return role_lookup.get(role.name, role.name.replace('_', ' ').title())
    legacy_role = user.groups.filter(name__in=['admin', 'director', 'secretary']).first()
    if legacy_role:
        return legacy_role.name.title()
    return 'Staff'
