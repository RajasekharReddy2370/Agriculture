from django.urls import path
from . import views

urlpatterns = [
    path("save-field/", views.save_field, name="save_field"),
    path("update-field/<int:field_id>/", views.update_field, name="update_field"),
    path("get-fields/", views.get_fields, name="get_fields"),
    path("search-field/", views.search_field, name="search_field"),
    path("field/<int:field_id>/blocks/", views.blocks_dashboard, name="blocks_dashboard"),
    path("field/<int:field_id>/get-blocks/", views.get_blocks, name="get_blocks"),
    path("field/<int:field_id>/save-block/", views.save_block, name="save_block"),
]