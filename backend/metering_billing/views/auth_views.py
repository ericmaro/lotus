import json
from ast import increment_lineno

import posthog
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_POST
from drf_spectacular.utils import extend_schema, inline_serializer
from lotus.settings import POSTHOG_PERSON
from metering_billing.models import Organization, User
from metering_billing.serializers.internal_serializers import *
from metering_billing.serializers.model_serializers import *
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


@require_POST
def login_view(request):

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {"detail": "Invalid JSON."}, status=status.HTTP_400_BAD_REQUEST
        )

    if data is None:
        return JsonResponse(
            {"detail": "No data provided."}, status=status.HTTP_400_BAD_REQUEST
        )

    username = data.get("username")
    password = data.get("password")

    if username is None or password is None:
        return JsonResponse(
            {"detail": "Please provide username and password."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(username=username, password=password)

    if user is None:
        return JsonResponse(
            {"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST
        )

    login(request, user)
    posthog.capture(
        POSTHOG_PERSON if POSTHOG_PERSON else user.organization.company_name,
        event="succesful login",
    )
    return JsonResponse({"detail": "Successfully logged in."})


@require_POST
def logout_view(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {"detail": "You're not logged in."}, status=status.HTTP_400_BAD_REQUEST
        )
    posthog.capture(
        POSTHOG_PERSON if POSTHOG_PERSON else request.user.organization.company_name,
        event="logout",
    )
    logout(request)
    return JsonResponse({"detail": "Successfully logged out."})


@ensure_csrf_cookie
def session_view(request):

    if not request.user.is_authenticated:

        return JsonResponse({"isAuthenticated": False})

    return JsonResponse({"isAuthenticated": True})


@ensure_csrf_cookie
def whoami_view(request):
    if not request.user.is_authenticated:
        return JsonResponse({"isAuthenticated": False})

    return JsonResponse({"username": request.user.username})


@extend_schema(
    request=RegistrationSerializer,
    responses={
        201: inline_serializer(
            "RegistrationResponse", fields={"detail": serializers.CharField()}
        )
    },
)
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reg_dict = serializer.validated_data["register"]
        existing_org_num = Organization.objects.filter(
            company_name=reg_dict["company_name"]
        ).count()
        if existing_org_num > 0:
            return JsonResponse(
                {"detail": "Organization already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        existing_user_num = User.objects.filter(username=reg_dict["username"]).count()
        if existing_user_num > 0:
            msg = f"User with username already exists"
            return JsonResponse({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)
        existing_user_num = User.objects.filter(email=reg_dict["email"]).count()
        if existing_user_num > 0:
            msg = f"User with email already exists"
            return JsonResponse({"detail": msg}, status=status.HTTP_400_BAD_REQUEST)
        org = Organization.objects.create(
            company_name=reg_dict["company_name"],
        )
        User.objects.create_user(
            email=reg_dict["email"],
            username=reg_dict["username"],
            password=reg_dict["password"],
            organization=org,
        )
        posthog.capture(
            POSTHOG_PERSON if POSTHOG_PERSON else org.company_name,
            event="register",
            properties={"company_name": reg_dict["company_name"]},
        )
        return JsonResponse(
            {"detail": "Successfully registered."}, status=status.HTTP_201_CREATED
        )