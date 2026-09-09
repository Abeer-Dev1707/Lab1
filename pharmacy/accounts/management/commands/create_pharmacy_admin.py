import os

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = "Create or configure the pharmacy administrator account."

    def handle(self, *args, **options):

        User = get_user_model()

        admin_username = os.getenv("ADMIN_USERNAME")
        admin_password = os.getenv("ADMIN_PASSWORD")

        if not admin_username:
            raise CommandError(
                "ADMIN_USERNAME is not set in the environment."
            )

        if not admin_password:
            raise CommandError(
                "ADMIN_PASSWORD is not set in the environment."
            )

        if len(admin_password) < 8:
            raise CommandError(
                "ADMIN_PASSWORD must contain at least 8 characters."
            )

        try:
            validate_password(admin_password)
        except ValidationError as error:
            raise CommandError(
                "The admin password does not meet Django's password "
                "requirements: "
                + " ".join(error.messages)
            )

        user = User.objects.filter(
            username=admin_username
        ).first()

        if user is None:

            user = User(
                username=admin_username,
                full_name="Abeer AL-Mufti",
                email="eng.abeer@gmail.com",
                phone="000000000",
                role="admin",
                account_status="approved",
                is_active=True,
                is_staff=True,
                is_superuser=True,
            )

            user.set_password(admin_password)
            user.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin account '{admin_username}' created successfully."
                )
            )

        else:

            user.full_name = "Abeer AL-Mufti"
            user.role = "admin"
            user.account_status = "approved"
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True

            user.set_password(admin_password)

            user.save(
                update_fields=[
                    "full_name",
                    "role",
                    "account_status",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "password",
                ]
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f"Admin account '{admin_username}' configured successfully."
                )
            )