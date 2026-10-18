from django.urls import path
from . import views

app_name = "quality"

urlpatterns = [
    path(
        "",
        views.inspection_list,
        name="inspection_list",
    ),
    path(
        "new/",
        views.inspection_create,
        name="inspection_create",
    ),
    path(
        "<int:pk>/",
        views.inspection_detail,
        name="inspection_detail",
    ),
]