# Generated by Django 2.1.2 on 2019-05-15 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisement', '0006_advertiser_favorite_ads'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisement',
            name='immediate',
            field=models.BooleanField(default=False),
        ),
    ]