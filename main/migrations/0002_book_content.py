# Generated by Django 4.2.6 on 2023-10-25 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='content',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
