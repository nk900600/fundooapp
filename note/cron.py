import datetime

from note.models import Notes

def my_scheduled_job():
    print(datetime.datetime.now())
    print("fff")
    reminder_list = []

    reminder_data = Notes.objects.filter(user_id=15, reminder__isnull=False).order_by('-reminder')
    print(reminder_data.values())
    reminder_list = reminder_data.values_list('reminder', flat=True)


