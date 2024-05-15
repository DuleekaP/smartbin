# firebase_listener.py
import firebase_admin
from firebase_admin import db
from .models import Bin
from django.utils import timezone

def listen_for_bin_level_changes():
    ref = db.reference('bin')

    def callback(event):
        bin_id = event.path.split('/')[-1]
        if isinstance(event.data, dict):
            new_level = event.data.get('level')
            if new_level == 0:
                try:
                    bin = Bin.objects.get(bin_id=bin_id)
                    bin.last_empty_date = timezone.now()
                    bin.save()
                except Bin.DoesNotExist:
                    pass

    # Register the callback function to listen for changes
    ref.listen(callback)