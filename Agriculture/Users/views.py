import logging

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import Details, Designation

logger = logging.getLogger(__name__)


def home(request):

    return render(
        request,
        "Users/home.html"
    )


def login_view(request):

    if request.method == "GET":

        return render(
            request,
            "Users/login.html"
        )

    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if not user:

        logger.warning(
            f"Invalid login for {username}"
        )

        return render(
            request,
            "Users/login.html",
            {
                "error": "Invalid Username or Password"
            }
        )

    login(request, user)

    logger.info(
        f"{username} logged in successfully"
    )

    return redirect("options")


def options(request):

    if not request.user.is_authenticated:
        return redirect("login")

    can_register = (
        request.user.is_superuser or
        (
            request.user.designation and
            request.user.designation.name in ["superuser","admin", "vc"]
        )
    )

    return render(
        request,
        "Users/options.html",
        {
            "can_register": can_register
        }
    )


def register(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if not (
        request.user.is_superuser or
        (
            request.user.designation and
            request.user.designation.name in ["superuser","admin", "vc"]
        )
    ):
        return redirect("options")

    if request.method == "POST":

        try:

            username = request.POST.get("username")

            if Details.objects.filter(
                username=username
            ).exists():

                return render(
                    request,
                    "Users/register.html",
                    {
                        "error": "Username already exists",
                        "designations": Designation.objects.all()
                    }
                )

            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if password != confirm_password:

                return render(
                    request,
                    "Users/register.html",
                    {
                        "error": "Passwords do not match",
                        "designations": Designation.objects.all()
                    }
                )

            designation = Designation.objects.get(
                id=request.POST.get("designation")
            )

            user = Details(

                username=username,
                firstname=request.POST.get("firstname"),
                lastname=request.POST.get("lastname"),
                nickname=request.POST.get("nickname"),
                email=request.POST.get("email"),
                personal_phone_number=request.POST.get("personal_phone_number"),
                home_phone_number=request.POST.get("home_phone_number"),
                bike=request.POST.get("bike"),
                address=request.POST.get("address"),
                designation=designation

            )

            image = request.FILES.get(
                "profilepic"
            )

            if image:

                user.profilepic = image.read()
                user.profilepic_content_type = image.content_type

            user.set_password(password)

            user.save()

            logger.info(
                f"{request.user.username} created user {username}"
            )

            return redirect("options")

        except Exception as e:

            logger.exception(str(e))

            return render(
                request,
                "Users/register.html",
                {
                    "error": str(e),
                    "designations": Designation.objects.all()
                }
            )

    return render(
        request,
        "Users/register.html",
        {
            "designations": Designation.objects.all()
        }
    )


def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    can_edit = (
        request.user.designation and
        request.user.designation.name in ["superuser","admin", "vc"]
    )

    return render(
        request,
        "Users/dashboard.html",
        {
            "can_edit": can_edit
        }
    )


def logout_view(request):

    username = request.user.username

    logout(request)

    logger.info(
        f"{username} logged out"
    )

    return redirect("home")