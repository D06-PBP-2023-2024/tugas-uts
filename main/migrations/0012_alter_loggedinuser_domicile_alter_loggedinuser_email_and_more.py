# Generated by Django 4.2.6 on 2023-10-28 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_merge_0009_tag_books_0010_loggedinuser_delete_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loggedinuser',
            name='domicile',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='loggedinuser',
            name='email',
            field=models.EmailField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='loggedinuser',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='loggedinuser',
            name='last_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='loggedinuser',
            name='phone_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
