# Generated by Django 3.2 on 2021-05-04 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_ugchords'),
    ]

    operations = [
        migrations.AddField(
            model_name='ugchords',
            name='capo',
            field=models.SmallIntegerField(default=0),
        ),
    ]
