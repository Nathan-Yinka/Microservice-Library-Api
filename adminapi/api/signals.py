from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Book
from .connections import RabbitMQClient

@receiver(post_save, sender=Book)
def handle_book_save(sender, instance, created, **kwargs):
    rabbitmq_client = RabbitMQClient()
    action = 'add' if created else 'update'
    book_data = {
        'action': action,
        'id': instance.id,
        'title': instance.title,
        'category': instance.category,
        'publisher': instance.publisher,
        "available": instance.available
    }
    rabbitmq_client.publish_message(book_data, 'book_updates')

@receiver(post_delete, sender=Book)
def handle_book_delete(sender, instance, **kwargs):
    rabbitmq_client = RabbitMQClient()
    book_data = {
        'action': 'remove',
        'id': instance.id
    }
    rabbitmq_client.publish_message(book_data, 'book_updates')
