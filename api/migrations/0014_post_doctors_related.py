# Generated by Django 5.1 on 2024-08-31 14:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_comment_author_alter_comment_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='doctors_related',
            field=models.ManyToManyField(blank=True, null=True, related_name='doctors_related', to=settings.AUTH_USER_MODEL),
        ),
    ]
