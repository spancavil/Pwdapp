# Generated by Django 4.0.3 on 2022-03-24 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pwdapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='user',
            field=models.CharField(max_length=500, unique=True),
        ),
    ]
