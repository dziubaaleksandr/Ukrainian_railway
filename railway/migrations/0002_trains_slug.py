# Generated by Django 4.2.2 on 2023-06-22 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('railway', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trains',
            name='slug',
            field=models.SlugField(default='None', max_length=255, verbose_name='URL'),
            preserve_default=False,
        ),
    ]
