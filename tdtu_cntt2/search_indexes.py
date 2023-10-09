from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_elasticsearch_dsl import fields,Document, Index

from .models import Application, ReceiverApplication

PUBLISHER_INDEX = Index('elastic')

@PUBLISHER_INDEX.doc_type
class ApplicationDocument(Document):
    id = fields.IntegerField(attr='id')
    title = fields.TextField(
        fields={
            "raw": {
                "type": "keyword"
            },
        }
    )
    pdf_content = fields.TextField(
        fields={
            "raw": {
                "type": "keyword"
            }
        }
    )
    content = fields.TextField(attr='content')
    sender_id = fields.IntegerField(attr='sender_id_id')
    delete_by_sender = fields.BooleanField(attr='delete_by_sender')
    user_receiver_id = fields.IntegerField(attr='get_user_receiver_id')
    class Django:
        model = Application

@receiver(post_save, sender=Application)
def update_application(sender, instance, **kwargs):
    if not instance.delete_by_sender:
        # print('update_application', instance)
        ApplicationDocument().update(instance, refresh=True)
@receiver(post_save, sender=Application)
def delete_application(sender, instance, **kwargs):
    if instance.delete_by_sender:
        # print('delete_application', instance)
        ApplicationDocument().update(instance, refresh=True)
        try:
            ApplicationDocument().get(id(instance.id)).delete(refresh=True)
        except:
            pass