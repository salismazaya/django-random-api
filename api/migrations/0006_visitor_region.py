# Generated by Django 3.2.5 on 2022-03-03 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_visitor_proccess_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='region',
            field=models.CharField(blank=True, max_length=3, null=True),
        ),
    ]
