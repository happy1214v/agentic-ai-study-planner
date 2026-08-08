from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Subject, StudyProgress
from .serializers import SubjectSerializer, StudyProgressSerializer
from .ai_service import generate_study_plan ,adjust_study_plan



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