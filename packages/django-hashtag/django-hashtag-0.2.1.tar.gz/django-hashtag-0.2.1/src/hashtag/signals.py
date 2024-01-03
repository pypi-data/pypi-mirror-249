import logging

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.utils import timezone

from hashtag.models import MyTag, MyTaggedItem

logger = logging.getLogger(__name__)


@receiver(post_save, sender=MyTaggedItem)
def increase_hashtag_count(sender, instance, **kwargs):
    try:
        logger.info(f"Signal fired: [increase_hashtag_count] for hashtag [{instance.tag}]")
        my_tag = MyTag.objects.get(id=instance.tag_id)
        instance.published = timezone.now()
        my_tag.count += 1
        my_tag.last_used = instance.published
        my_tag.save()
    except Exception as err:
        logger.error(f"Hashtag signal: {err}")


@receiver(post_delete, sender=MyTaggedItem)
def decrease_hashtag_count(sender, instance, **kwargs):
    try:
        logger.info(f"Signal fired: [decrease_hashtag_count] for hashtag [{instance.tag}]")
        my_last_tag = MyTaggedItem.objects.filter(tag_id=instance.tag_id).order_by(
            "-id"
        )[:1]
        my_tag = MyTag.objects.get(id=instance.tag_id)
        my_tag.count -= 1
        if my_last_tag:
            my_tag.last_used = my_last_tag[0].published
        else:
            my_tag.last_used = timezone.datetime(2000, 1, 1, 00, 00)
        my_tag.save()
    except Exception as err:
        logger.error(f"Hashtag signal: {err}")
