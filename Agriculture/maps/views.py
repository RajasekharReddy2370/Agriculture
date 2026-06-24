import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Field

def can_manage_fields(user):
    """Helper to check if a user can create or update fields."""
    return (
        user.is_authenticated and
        user.designation and
        user.designation.name in ["superuser","admin", "vc"]
    )

def get_fields(request):
    """Allows ALL authenticated users (including Supervisor and People) to view map data."""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Authentication required"}, status=401)

    fields = Field.objects.all()
    data = []

    for field in fields:
        data.append({
            "field_id": field.id,
            "field_name": field.field_name,
            "coordinates": field.coordinates,
            "created_by": field.created_by.username if field.created_by else None,
            "updated_by": field.updated_by.username if field.updated_by else None,
            "created_at": field.created_at,
            "updated_at": field.updated_at
        })

    return JsonResponse({"success": True, "data": data})

def save_field(request):
    """Restricted to superuser,admin and vc via standard CSRF protection."""
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)
        
    if not can_manage_fields(request.user):
        return JsonResponse({"success": False, "message": "Permission denied"}, status=403)

    try:
        data = json.loads(request.body)
        field = Field.objects.create(
            field_name=data["field_name"],
            coordinates=data["coordinates"],
            created_by=request.user
        )
        return JsonResponse({"success": True, "message": "Field saved successfully", "field_id": field.id})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)

def update_field(request, field_id):
    """Restricted to admin and vc via standard CSRF protection."""
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)

    if not can_manage_fields(request.user):
        return JsonResponse({"success": False, "message": "Permission denied"}, status=403)

    try:
        data = json.loads(request.body)
        field = Field.objects.get(id=field_id)
        
        field.field_name = data["field_name"]
        field.coordinates = data["coordinates"]
        field.updated_by = request.user
        field.save()

        return JsonResponse({"success": True, "message": "Field updated successfully", "field_id": field.id})
    except Field.DoesNotExist:
        return JsonResponse({"success": False, "message": "Field not found"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)

def search_field(request):
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Authentication required"}, status=401)

    field_name = request.GET.get("field_name", "")
    fields = Field.objects.filter(field_name__icontains=field_name)
    
    data = [{"field_id": f.id, "field_name": f.field_name, "coordinates": f.coordinates} for f in fields]
    return JsonResponse({"success": True, "data": data})