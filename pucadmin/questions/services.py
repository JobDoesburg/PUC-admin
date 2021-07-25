from django.utils import timezone

from PUCadmin.utils import send_email


def notify_new_assignee(question):
    if not question.assignee or question.assignee.notification_email is None:
        return

    email = question.assignee.notification_email
    subject = f"[PUC admin] A new question ({question.id}) was assigned to you"
    send_email(
        email,
        subject,
        "email/question-assigned.txt",
        {"question": question, "assigned_date": timezone.now()},
    )
