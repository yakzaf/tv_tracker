# Generated by Django 3.0.8 on 2020-11-06 16:48

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usershowlist',
            options={'ordering': ('date_added',)},
        ),
        migrations.AddField(
            model_name='show',
            name='kind',
            field=models.CharField(default=None, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='overview',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='show',
            name='year',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='picture_url',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='show',
            name='service',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), size=None),
        ),
    ]
