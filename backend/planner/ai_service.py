import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_study_plan(subject, exam_date, hours):
    prompt = f"""
Create a day-by-day study plan.

Subject: {subject}
Exam Date: {exam_date}
Daily Study Hours: {hours}

Include revision before the exam.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


def adjust_study_plan(subject, exam_date, daily_hours, progress_data):
    prompt = f"""
You are an intelligent study planning agent.

Create an adjusted day-by-day study plan based on the student's
actual study progress.

Subject: {subject}
Exam Date: {exam_date}
Daily Study Hours: {daily_hours}

Student Progress:
{progress_data}

Analyze:
1. Planned study hours
2. Completed study hours
3. Topics already completed
4. Missed study hours
5. Remaining time before exam

Then create a realistic adjusted study plan.

Include:
- Remaining topics
- Revision
- Practice questions
- Extra time for missed topics
- Exam-day revision

Return only the study plan.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content