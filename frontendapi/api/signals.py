from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User,BorrowedBook
from .connections import RabbitMQClient

@receiver(post_save, sender=User)
def publish_user_changes(sender, instance, created, **kwargs):
    rabbitmq_client = RabbitMQClient()
    user_data = {
        'id': instance.id,
        'email': instance.email,
        'first_name': instance.first_name,
        'last_name': instance.last_name
    }
    rabbitmq_client.publish_message(user_data, 'user_updates')


@receiver(post_save, sender=BorrowedBook)
def publish_borrowed_book_changes(sender, instance, created, **kwargs):
    rabbitmq_client = RabbitMQClient()
    status = "borrow" if not instance.is_returned else "return"
    borrow_data = {
            'status': status,
            'id': instance.id,
            'user_id': instance.user.id,
            'book_id': instance.book.id,
            'number_of_days': instance.number_of_days,
            'borrowed_on': instance.borrowed_on.isoformat(),
            'return_date': instance.return_date.isoformat(),
            'is_returned': instance.is_returned
        }
    rabbitmq_client.publish_message(borrow_data, 'borrow_updates')