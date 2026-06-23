from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("logout/", views.logout_view, name="logout"),
]


# {
#     "username": "Raja",
#     "firstname": "RajasekharReddy",
#     "lastname": "Kasireddy",
#     "nickname": "Raj",
#     "email": "raja@gmail.com",
#     "personal_phone_number": "2370",
#     "home_phone_number": "2370",
#     "bike": "BOXER",
#     "designation_id": 2,
#     "password": "2370"
# }