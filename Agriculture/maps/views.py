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

import json
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Field, Block

def blocks_dashboard(request, field_id):
    """Opens the dedicated blocks page for the selected field."""
    if not request.user.is_authenticated:
        return redirect("login")
        
    # Fetch the exact field (like "thota") or return a 404 error if not found
    field = get_object_or_404(Field, id=field_id)
    
    # Check if the user has permission to draw blocks
    can_edit = request.user.designation and request.user.designation.name in ["Admin", "VC"]
    
    return render(request, "Users/blocks.html", {
        "field": field,
        "can_edit": can_edit
    })

def get_blocks(request, field_id):
    """API to load any existing blocks already drawn inside this field."""
    blocks = Block.objects.filter(field_id=field_id)
    data = [{
        "block_id": b.id,
        "block_name": b.block_name,
        "coordinates": b.coordinates
    } for b in blocks]
    return JsonResponse({"success": True, "data": data})

def save_block(request, field_id):
    """API to save a newly drawn block layout inside this field."""
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Method not allowed"}, status=405)
        
    try:
        data = json.loads(request.body)
        field = Field.objects.get(id=field_id)
        
        block = Block.objects.create(
            field=field,
            block_name=data["block_name"],
            coordinates=data["coordinates"]
        )
        return JsonResponse({"success": True, "block_id": block.id})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=400)
    

def update_details(request, field_id):
    if request.method == "POST":
        try:
            # Look up the field using its database ID
            field = get_object_or_404(Field, id=field_id)
            data = json.loads(request.body)
            
            # Extract and update data from the sidebar inputs
            field.work_type = data.get('work_type', 'Ploughing')
            field.crop_type = data.get('crop_type', 'Rice')
            
            # Handle empty land string elegantly
            acres_value = data.get('acres', '').strip()
            field.acres = float(acres_value) if acres_value else None
            
            field.save()
            return JsonResponse({"success": True})
            
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})
            
    return JsonResponse({"success": False, "message": "Invalid request method."})