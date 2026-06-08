from django.core.management.base import BaseCommand

from auth_app.models import (
    User,
    Action,
    Role,
    Resource,
    Permission,
    UserRole,
    RolePermission,
)


class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        roles = {}

        for role_name in (
            'admin',
            'teacher',
            'student',
            'parent',
        ):
            role, _ = Role.objects.get_or_create(
                name=role_name
            )
            roles[role_name] = role

        actions = {}

        for action_name in (
            'GET',
            'POST',
            'PUT',
            'PATCH',
            'DELETE',
        ):
            action, _ = Action.objects.get_or_create(
                name=action_name
            )
            actions[action_name] = action

        resources = {}

        for resource_name in (
            'user',
            'action',
            'resourse',
            'permission',
            'role',
            'user_role',
            'role_permission',
            'graduate',
            'subject',
            'refresh_token',
        ):
            resource, _ = Resource.objects.get_or_create(
                name=resource_name
            )
            resources[resource_name] = resource

        permissions = {}

        for resource in resources.values():
            for action in actions.values():

                permission, _ = (
                    Permission.objects.get_or_create(
                        resource=resource,
                        action=action,
                    )
                )

                permissions[
                    f'{resource.name}.{action.name}'
                ] = permission

        for permission in Permission.objects.all():
            RolePermission.objects.get_or_create(
                role=roles['admin'],
                permission=permission,
            )

        student_permissions = [
            'graduate.GET',
            'subject.GET',
        ]

        for code in student_permissions:
            RolePermission.objects.get_or_create(
                role=roles['student'],
                permission=permissions[code],
            )

        admin, _ = User.objects.get_or_create(
            email='dayan@example.com',
            defaults={
                'first_name': 'Dayan',
                'last_name': 'Iskhakov',
            },
        )

        admin.set_password('dayan123')

        student, _ = User.objects.get_or_create(
            email='iskhak@example.com',
            defaults={
                'first_name': 'Iskhak',
                'last_name': 'Dayanov',
            },
        )

        student.set_password('iskhak123')

        UserRole.objects.get_or_create(
            user=admin,
            role=roles['admin'],
        )

        UserRole.objects.get_or_create(
            user=student,
            role=roles['student'],
        )

        self.stdout.write(
            self.style.SUCCESS(
                'RBAC data seeded successfully'
            )
        )
