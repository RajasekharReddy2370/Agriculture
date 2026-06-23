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

@csrf_exempt
def register(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "success": False,
                "message": "Method not allowed"
            },
            status=405
        )

    try:

        username = request.POST.get("username")

        if Details.objects.filter(username=username).exists():

            return JsonResponse(
                {
                    "success": False,
                    "message": "Username already exists"
                },
                status=400
            )

        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:

            return JsonResponse(
                {
                    "success": False,
                    "message": "Passwords do not match"
                },
                status=400
            )

        designation = Designation.objects.get(
            id=request.POST.get("designation")
        )

        user = Details.objects.create(
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

        user.set_password(password)
        user.save()

        return JsonResponse(
            {
                "success": True,
                "message": "User registered successfully",
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "designation": user.designation.name
                }
            }
        )

    except Exception as e:

        logger.exception(str(e))

        return JsonResponse(
            {
                "success": False,
                "message": str(e)
            },
            status=500
        )

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
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

        return render(
            request,
            "Users/login.html",
            {
                "error": "Invalid credentials"
            }
        )

    login(request, user)

    return redirect("dashboard")

# def dashboard(request):

#     if not request.user.is_authenticated:
#         logger.warning("Unauthenticated user tried to access dashboard")
#         return redirect("login")

#     logger.info(f"Dashboard accessed by {request.user.username}")

#     return render(request, "Users/dashboard.html")

def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    can_edit = (
        request.user.designation and
        request.user.designation.name in ["Admin", "VC"]
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

    logger.info(f"User logged out: {username}")

    return redirect("home")


