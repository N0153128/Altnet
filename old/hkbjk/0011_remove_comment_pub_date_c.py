# Generated by Django 2.2.5 on 2019-10-15 00:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HikkaHq', '0010_auto_20191015_0100'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='pub_date_c',
        ),
    ]
