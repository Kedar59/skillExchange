# Generated by Django 4.2.5 on 2023-10-17 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_credential'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='credebility_score',
            field=models.IntegerField(default=0),
        ),
    ]
