# Generated by Django 3.2 on 2021-05-05 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_ugchords_capo'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChromaToChord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('C', models.DecimalField(decimal_places=9, default=0, max_digits=10)),
                ('Cs', models.DecimalField(decimal_places=9, default=0, max_digits=10)),
                ('D', models.DecimalField(decimal_places=9, default=0, max_digits=10)),
                ('Ds', models.DecimalField(decimal_places=9, default=0, max_digits=10)),
                ('E', models.DecimalField(decimal_places=9, default=0, max_digits=10)),
                ('F', models.DecimalField(decimal_places=9, default=0, max_digits=10)),
                ('Fs', models.DecimalField(decimal_places=9, default=0, max_digits=10)),
                ('G', models.DecimalField(decimal_places=9, default=0, max_digits=10)),
                ('Gs', models.DecimalField(decimal_places=9, default=0, max_digits=10)),
                ('A', models.DecimalField(decimal_places=9, default=0, max_digits=10)),
                ('As', models.DecimalField(decimal_places=9, default=0, max_digits=10)),
                ('B', models.DecimalField(decimal_places=9, default=0, max_digits=10)),
                ('chord', models.TextField()),
                ('cleaned_chord', models.TextField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
