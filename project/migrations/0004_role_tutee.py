# Generated by Django 3.2.3 on 2021-07-23 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20210723_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='tutee',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
