from django.shortcuts import render
from production.models import ProductionJob
from quality.models import Inspection

def dashboard_home(request):
    total_jobs = ProductionJob.objects.count()
    
    pending_jobs = ProductionJob.objects.filter(
        status="PENDING"
    ).count()
    
    in_progress_jobs = ProductionJob.objects.filter(
        status="IN_PROGRESS"
    ).count()

    approved_jobs = ProductionJob.objects.filter(
        status="APPROVED"
    ).count()

    rejected_jobs = ProductionJob.objects.filter(
        status="REJECTED"
    ).count()

    total_inspections = Inspection.objects.count()

    passed_inspections = Inspection.objects.filter(
        result="PASS"
    ).count()

    failed_inspections = Inspection.objects.filter(
        result="FAIL"
    ).count()

    recent_jobs = ProductionJob.objects.order_by(
        "-created_at"
    )[:5]

    context = {
        "total_jobs": total_jobs,
        "pending_jobs": pending_jobs,
        "in_progress_jobs": in_progress_jobs,
        "approved_jobs": approved_jobs,
        "rejected_jobs": rejected_jobs,
        "total_inspections": total_inspections,
        "passed_inspections": passed_inspections,
        "failed_inspections": failed_inspections,
        "recent_jobs": recent_jobs,
    }

    return render(request, "dashboard/home.html", context)

