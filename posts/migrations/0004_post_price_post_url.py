# Generated by Django 4.2.5 on 2023-11-21 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='price',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
