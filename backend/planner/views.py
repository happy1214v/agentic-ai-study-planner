from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Subject, StudyProgress
from .serializers import SubjectSerializer, StudyProgressSerializer
from .ai_service import generate_study_plan ,adjust_study_plan
from datetime import date


class SubjectListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


class StudyPlanView(APIView):

    def post(self, request):

        subject = request.data.get("subject")
        exam_date = request.data.get("exam_date")
        hours = request.data.get("hours")

        if not subject or not exam_date or not hours:
            return Response(
                {
                    "error": "subject, exam_date and hours are required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        study_plan = generate_study_plan(
            subject,
            exam_date,
            hours
        )

        return Response(
            {
                "subject": subject,
                "exam_date": exam_date,
                "daily_hours": hours,
                "study_plan": study_plan
            }
        )


class ProgressView(APIView):

    def post(self, request):

        serializer = StudyProgressSerializer(data=request.data)

        if serializer.is_valid():
            progress = serializer.save()

            return Response(
                {
                    "message": "Study progress saved successfully",
                    "progress": StudyProgressSerializer(progress).data
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class AdjustPlanView(APIView):

    def post(self, request):

        subject_id = request.data.get("subject_id")

        if not subject_id:
            return Response(
                {
                    "error": "subject_id is required"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            subject = Subject.objects.get(id=subject_id)
        except Subject.DoesNotExist:
            return Response(
                {
                    "error": "Subject not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        progress = StudyProgress.objects.filter(
            subject=subject
        ).order_by("study_date")

        progress_data = []

        for item in progress:
            progress_data.append({
                "date": str(item.study_date),
                "planned_hours": item.planned_hours,
                "completed_hours": item.completed_hours,
                "completed_topic": item.completed_topic,
                "notes": item.notes
            })

        adjusted_plan = adjust_study_plan(
            subject.name,
            str(subject.exam_date),
            subject.daily_study_hours,
            progress_data
        )

        return Response({
            "subject": subject.name,
            "exam_date": str(subject.exam_date),
            "adjusted_plan": adjusted_plan
        })




class DashboardView(APIView):

    def get(self, request):

        subjects = Subject.objects.all()

        total_subjects = subjects.count()

        today = date.today()

        today_progress = StudyProgress.objects.filter(
            study_date=today
        )

        today_planned_hours = sum(
            item.planned_hours
            for item in today_progress
        )

        today_completed_hours = sum(
            item.completed_hours
            for item in today_progress
        )

        if today_planned_hours > 0:
            progress_percentage = round(
                (today_completed_hours / today_planned_hours) * 100,
                2
            )
        else:
            progress_percentage = 0

        upcoming_subject = subjects.filter(
            exam_date__gte=today
        ).order_by("exam_date").first()

        if upcoming_subject:
            next_exam = str(upcoming_subject.exam_date)
            days_remaining = (
                upcoming_subject.exam_date - today
            ).days
        else:
            next_exam = None
            days_remaining = None

        return Response({
            "total_subjects": total_subjects,
            "today_planned_hours": today_planned_hours,
            "today_completed_hours": today_completed_hours,
            "progress_percentage": progress_percentage,
            "next_exam": next_exam,
            "days_remaining": days_remaining
        })