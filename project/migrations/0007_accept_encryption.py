# Generated by Django 3.2.3 on 2021-07-24 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0006_accept'),
    ]

    operations = [
        migrations.AddField(
            model_name='accept',
            name='encryption',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]