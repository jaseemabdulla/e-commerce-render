# Generated by Django 4.2.3 on 2023-07-24 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cart', '0005_remove_useraddress_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraddress',
            name='user',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL),
        ),
    ]
