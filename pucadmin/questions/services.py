from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

def notify_new_assignee(question):
    if not question.assignee or question.assignee.notification_email is None:
        return

    email = question.assignee.notification_email
    subject = f"[PUC admin] A new question {question.id} was assigned to you"
    message = f"You were assigned a question by PUC admin.\n" \
              f"The question was submitted at {question.created_at:%d-%m-%Y %H:%M} " \
              f"for the course {question.course.name} by " \
              f"{question.students_text} ({question.school}) " \
              f"and assigned to you at {timezone.now():%d-%m-%Y %H:%M}:" \
              f"\n\n\t{question.message}\n\n" \
              f"Research question:\n\t{question.research_question}\n\n" \
              f"Sub questions:\n\t{question.sub_questions}\n\n" \
              f"Do not forget to mark this question as `completed` when it has been answered!\n\n" \
              f"_This email was sent automatically_"
    send_mail(subject, message, from_email=settings.EMAIL_DEFAULT_SENDER, recipient_list=[email])
