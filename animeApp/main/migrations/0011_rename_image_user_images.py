# Generated by Django 5.0.3 on 2024-08-30 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_user_bio_user_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='image',
            new_name='images',
        ),
    ]
