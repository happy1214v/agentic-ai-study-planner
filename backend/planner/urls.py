from django.urls import path
from .views import (
    SubjectListView,
    StudyPlanView,
    ProgressView,
    AdjustPlanView,
    DashboardView
)
urlpatterns = [
    path("subjects/", SubjectListView.as_view(), name="subjects"),
    path("study-plan/", StudyPlanView.as_view(), name="study-plan"),
    path("progress/", ProgressView.as_view(), name="progress"),
    path("adjust-plan/", AdjustPlanView.as_view(), name="adjust-plan"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]