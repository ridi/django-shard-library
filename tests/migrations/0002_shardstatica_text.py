# Generated by Django 2.0.2 on 2018-05-24 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shardstatica',
            name='text',
            field=models.CharField(max_length=32, null=True),
        ),
    ]