from auth_app.models import (
    User,
    Action,
    Role,
    Resource,
    Permission,
    UserRole,
    RolePermission,
)

ACTIONS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

ROLES = ['admin', 'teacher', 'student', 'parent']

RESOURCES = [
    'user',
    'action',
    'resource',
    'permission',
    'role',
    'user_role',
    'role_permission',
    'graduate',
    'subject',
    'refresh_token',
]


def init_rbac_models():
    Action.objects.bulk_create(
        [Action(name=name) for name in ACTIONS],
        ignore_conflicts=True,
    )

    Role.objects.bulk_create(
        [Role(name=name) for name in ROLES],
        ignore_conflicts=True,
    )

    Resource.objects.bulk_create(
        [Resource(name=name) for name in RESOURCES],
        ignore_conflicts=True,
    )

    Permission.objects.bulk_create(
        [
            Permission(resource=resource, action=action)
            for resource in Resource.objects.all()
            for action in Action.objects.all()
        ],
        ignore_conflicts=True,
    )

    admin_role = Role.objects.get(name='admin')
    student_role = Role.objects.get(name='student')

    permissions = Permission.objects.all()

    RolePermission.objects.bulk_create(
        [
            RolePermission(role=admin_role, permission=permission)
            for permission in permissions
        ],
        ignore_conflicts=True,
    )

    student_permissions = permissions.filter(
        resource__name__in=['graduate', 'subject'],
        action__name='GET',
    )

    RolePermission.objects.bulk_create(
        [
            RolePermission(role=student_role, permission=permission)
            for permission in student_permissions
        ],
        ignore_conflicts=True,
    )

    admin, _ = User.objects.get_or_create(
        email='admin@example.com',
        defaults={
            'first_name': 'Admin',
            'last_name': 'User',
        },
    )

    student, _ = User.objects.get_or_create(
        email='student@example.com',
        defaults={
            'first_name': 'Student',
            'last_name': 'User',
        },
    )

    admin.set_password('admin123')
    student.set_password('student123')

    UserRole.objects.get_or_create(
        user=admin,
        role=admin_role,
    )

    UserRole.objects.get_or_create(
        user=student,
        role=student_role,
    )

    print('db seeded')
