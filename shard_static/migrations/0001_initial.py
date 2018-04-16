# Generated by Django 2.0.2 on 2018-04-11 10:26

from django.db import migrations, models
import shard_static.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StaticSyncStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('static_model_key', models.CharField(max_length=64, unique=True, verbose_name='Static Model Key')),
                ('last_modified', models.DateTimeField(null=True, verbose_name='Last Modified')),
            ],
            options={
                'db_table': 'static_sync_status',
            },
            bases=(shard_static.mixins.ShardStaticMixin, models.Model),
        ),
    ]