# Generated by Django 4.2 on 2025-05-25 19:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0014_alter_reject_receiver_alter_reject_sender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='winks',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_winks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='winks',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_winks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='winks',
            unique_together={('sender', 'receiver')},
        ),
    ]
