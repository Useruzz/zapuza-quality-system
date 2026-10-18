from django.urls import path
from . import views

app_name = "production"

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("jobs/new/", views.job_create, name="job_create"),
    path("jobs/<int:pk>/", views.job_detail, name="job_detail"),
    path(
        "jobs/<int:pk>/status/",
        views.update_job_status,
        name="update_job_status",
    ),
]