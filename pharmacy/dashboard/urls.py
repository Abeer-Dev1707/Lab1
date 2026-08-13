from django.urls import path
from . import views

urlpatterns = [

    path("login/", views.login_view, name="login"),

    path("dashboard/", views.home, name="dashboard"),

    path("logout/", views.logout_view, name="logout"),

    path("about/", views.about, name="about"),

    path("contact/", views.contact, name="contact"),

    path("forgot-password/", views.forgot_password, name="forgot_password"),

    path("404/", views.page_not_found, name="page404"),

]