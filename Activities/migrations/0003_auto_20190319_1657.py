# Generated by Django 2.1.7 on 2019-03-19 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Activities', '0002_auto_20190306_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentence',
            name='datecreated',
            field=models.DateField(db_column='DateCreated', null=True),
        ),
    ]
