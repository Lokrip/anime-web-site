# Generated by Django 5.0.3 on 2024-08-25 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_animeview_viewed_at'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='animeview',
            unique_together=set(),
        ),
    ]
