import json
import logging
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import Details, Designation

logger = logging.getLogger(__name__)

def home(request):
    return render(request, "Users/home.html")

def register(request):

    logger.info("Register page accessed")

    if request.method == "POST":

        try:
            username = request.POST.get("username")

            logger.info(f"Registration request received for username={username}")

            if Details.objects.filter(username=username).exists():
                logger.warning(f"Username already exists: {username}")

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
                logger.warning(f"Password mismatch for username={username}")

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
                designation=designation
            )

            image = request.FILES.get("profilepic")

            if image:
                user.profilepic = image.read()
                user.profilepic_content_type = image.content_type
                logger.info(f"Profile picture uploaded for {username}")

            user.set_password(password)
            user.save()

            logger.info(f"User registered successfully: {username}")

            return redirect("login")

        except Exception as e:
            logger.exception(f"Registration failed: {str(e)}")

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
        {"designations": Designation.objects.all()}
    )

def login_view(request):

    logger.info("Login page accessed")

    if request.method == "POST":

        username = request.POST.get("username")

        logger.info(f"Login attempt for username={username}")

        user = authenticate(
            request,
            username=username,
            password=request.POST.get("password")
        )

        if user:
            login(request, user)

            logger.info(f"Login successful for username={username}")

            return redirect("dashboard")

        logger.warning(f"Invalid login attempt for username={username}")

        return render(
            request,
            "Users/login.html",
            {"error": "Invalid credentials"}
        )

    return render(request, "Users/login.html")

def dashboard(request):

    if not request.user.is_authenticated:
        logger.warning("Unauthenticated user tried to access dashboard")
        return redirect("login")

    logger.info(f"Dashboard accessed by {request.user.username}")

    return render(request, "Users/dashboard.html")

def logout_view(request):

    username = request.user.username

    logout(request)

    logger.info(f"User logged out: {username}")

    return redirect("home")


