from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=100)
    exam_date = models.DateField()
    daily_study_hours = models.PositiveIntegerField(default=2)

    def __str__(self):
        return self.name


class StudyProgress(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="progress"
    )
    study_date = models.DateField(auto_now_add=True)
    planned_hours = models.PositiveIntegerField(default=2)
    completed_hours = models.PositiveIntegerField(default=0)
    completed_topic = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject.name} - {self.study_date}"