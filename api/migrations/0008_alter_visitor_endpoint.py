# Generated by Django 3.2.5 on 2022-03-03 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_rename_region_visitor_country_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='endpoint',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]