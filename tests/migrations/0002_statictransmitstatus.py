# Generated by Django 2.0.2 on 2018-06-07 12:22

from django.db import migrations, models
import shard.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StaticTransmitStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=64, unique=True, verbose_name='Transmit Status Key')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created Datetime')),
                ('last_modified', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('criterion_id', models.IntegerField(default=1, verbose_name='Criterion ID')),
            ],
            options={
                'abstract': False,
            },
            bases=(shard.mixins.IsolatedShardMixin, models.Model),
        ),
    ]