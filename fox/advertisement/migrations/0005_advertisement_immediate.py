# Generated by Django 2.1.2 on 2019-05-15 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0004_auto_20190514_2020'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='immediate',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
