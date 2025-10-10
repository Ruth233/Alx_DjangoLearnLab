from django.contrib.contenttypes.models import ContentType
from .models import Notification

def create_notification(actor, recipient, verb, target=None):
    """
    Generic helper to create a notification.
    """
    ct = None
    oid = None
    if target is not None:
        ct = ContentType.objects.get_for_model(target.__class__)
        oid = target.pk
    Notification.objects.create(
        recipient=recipient,
        actor=actor,
        verb=verb,
        target_content_type=ct,
        target_object_id=str(oid) if oid is not None else None
    )

def create_notification_for_like(actor, recipient, target):
    create_notification(actor=actor, recipient=recipient, verb='liked your post', target=target)

def create_notification_for_follow(actor, recipient):
    create_notification(actor=actor, recipient=recipient, verb='started following you', target=None)

def create_notification_for_comment(actor, recipient, target):
    create_notification(actor=actor, recipient=recipient, verb='commented on your post', target=target)
