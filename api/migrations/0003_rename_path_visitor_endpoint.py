# Generated by Django 3.2.5 on 2022-03-03 02:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20220303_0945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visitor',
            old_name='path',
            new_name='endpoint',
        ),
    ]