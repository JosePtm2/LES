# Generated by Django 2.1.7 on 2019-03-20 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Processes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='data_creation',
            field=models.DateField(db_column='Data Creation', null=True),
        ),
    ]
