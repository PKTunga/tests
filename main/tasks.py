# from celery import shared_task
from main.models import VPS, Usage
from utils.ec2 import client
from datetime import timedelta, datetime
# from celery import shared_task
import datetime
from datetime import timezone

def check_for_instances_and_stop_them():
  try:
    date = datetime.datetime.today() - timedelta(hours=2, minutes=54)
    instances = VPS.objects.filter(current_usage__start_date__lt=date)
    print(instances)
    print(date)
    for instance in instances:
        insta = VPS.objects.get(id=instance.id)
        cli= client(insta.template)
        try:
          status = insta.stop(cli)
          usage = insta.current_usage
          usage.stop_date = datetime.datetime.now(tz=timezone.utc)
          usage.description = 'Auto Stop'
          usage.save()
          insta.current_usage = None
          insta.save()
        except Exception as e:
          pass
    return 
  except Exception as e:
    print(e)
    return 