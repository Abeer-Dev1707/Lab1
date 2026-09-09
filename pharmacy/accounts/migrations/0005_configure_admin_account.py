from django.db import migrations
from django.contrib.auth.hashers import make_password


ADMIN_USERNAME = "Abeer_Ahmed"


def configure_pharmacy_admin(apps, schema_editor):
    UserModel = apps.get_model("accounts", "User")

    db_alias = schema_editor.connection.alias
    User = UserModel.objects.using(db_alias)

    user = User.filter(username=ADMIN_USERNAME).first()

    if user is None:
        User.create(
            username=ADMIN_USERNAME,
            full_name="Abeer AL-Mufti",
            email="eng.abeer@gmail.com",
            phone="000000000",
            role="admin",
            account_status="approved",
            is_active=True,
            is_staff=True,
            is_superuser=True,

            # لا توجد كلمة مرور حقيقية هنا.
            # سيتم تعيينها لاحقًا من خلال
            # create_pharmacy_admin
            password=make_password(None),
        )

    else:
        user.role = "admin"
        user.account_status = "approved"
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True

        user.save(
            update_fields=[
                "role",
                "account_status",
                "is_active",
                "is_staff",
                "is_superuser",
            ]
        )


def reverse_configure_pharmacy_admin(apps, schema_editor):
    UserModel = apps.get_model("accounts", "User")

    db_alias = schema_editor.connection.alias
    User = UserModel.objects.using(db_alias)

    user = User.filter(username=ADMIN_USERNAME).first()

    if user:
        user.is_staff = False
        user.is_superuser = False

        user.save(
            update_fields=[
                "is_staff",
                "is_superuser",
            ]
        )


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_managerprofile"),
    ]

    operations = [
        migrations.RunPython(
            configure_pharmacy_admin,
            reverse_configure_pharmacy_admin,
        ),
    ]