# Generated by Django 4.2.4 on 2023-10-27 09:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_tag_books'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='books',
        ),
    ]