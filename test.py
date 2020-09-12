from timetracker.models import Attandance
from django.utils import timezone
import datetime


def auto_end_work():
    result = Attandance.objects.all().order_by(
        'employee', '-created_at').distinct('employee')
    for row in result:
        if row.gsheet_type == 'start':
            difference = timezone.now() - row.created_at
            if difference >= datetime.timedelta(hours=12):
                # add new field to attandance
                print(difference)


auto_end_work()
