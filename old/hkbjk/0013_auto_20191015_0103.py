# Generated by Django 2.2.5 on 2019-10-15 00:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('HikkaHq', '0012_comment_pub_date_c'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='pub_date_c',
            new_name='pub_date',
        ),
    ]
