import json

from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from inventory.serializers import FileSerializer

from inventory.models import File, ParsingStatus


@receiver(post_save, sender=File)
def create_new_file(sender, instance, **kwargs):
    ParsingStatus.objects.create(file=instance)
    file = {
        'id': instance.id,
        'name': instance.file_name,
        'file': str(instance.file),
        'user': instance.user.username,
        'status': instance.status.status
    }
    # file = 'new_file'
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        'main_page',
        {
            'type': 'new_file',
            'text': {'event': 'new file',
                     'file': file}
        }
    )


