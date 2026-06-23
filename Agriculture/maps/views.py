from django.views.decorators.csrf import csrf_exempt

def can_manage_fields(user):

    return (
        user.is_authenticated and
        user.designation and
        user.designation.name in ["Admin", "VC"]
    )

import json

from django.http import JsonResponse
from .models import Field

@csrf_exempt
def save_field(request):
    if not can_manage_fields(request.user):
        return JsonResponse(
            {"message": "Permission denied"},
            status=403
        )

    data = json.loads(request.body)

    field = Field.objects.create(
        field_name=data["field_name"],
        coordinates=data["coordinates"],
        created_by=request.user
    )

    return JsonResponse(
        {
            "success": True,
            "message": "Field saved successfully",
            "field_id": field.id
        }
    )

@csrf_exempt
def update_field(request, field_id):

    if not can_manage_fields(request.user):
        return JsonResponse(
            {
                "success": False,
                "message": "Permission denied"
            },
            status=403
        )

    data = json.loads(request.body)

    field = Field.objects.get(id=field_id)

    field.field_name = data["field_name"]
    field.coordinates = data["coordinates"]

    field.updated_by = request.user

    field.save()

    return JsonResponse(
        {
            "success": True,
            "message": "Field updated successfully",
            "field_id": field.id
        }
    )

@csrf_exempt
def get_fields(request):

    if not can_manage_fields(request.user):
        return JsonResponse(
            {
                "success": False,
                "message": "Permission denied"
            },
            status=403
        )

    fields = Field.objects.all()

    data = []

    for field in fields:

        data.append(
            {
                "field_id": field.id,
                "field_name": field.field_name,
                "coordinates": field.coordinates,
                "created_by": field.created_by.username if field.created_by else None,
                "updated_by": field.updated_by.username if field.updated_by else None,
                "created_at": field.created_at,
                "updated_at": field.updated_at
            }
        )

    return JsonResponse(
        {
            "success": True,
            "data": data
        }
    )

from django.http import JsonResponse


from django.http import JsonResponse

def search_field(request):

    field_name = request.GET.get("field_name", "")

    fields = Field.objects.filter(
        field_name__icontains=field_name
    )

    data = []

    for field in fields:

        data.append(
            {
                "field_id": field.id,
                "field_name": field.field_name,
                "coordinates": field.coordinates
            }
        )

    return JsonResponse(
        {
            "success": True,
            "data": data
        }
    )