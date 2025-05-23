# Generated by Django 5.1.6 on 2025-05-21 16:29

import django.db.models.deletion
import django_extensions.db.fields
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proxy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvailabilitySlot',
            fields=[
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('internal_uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
                ('is_available', models.BooleanField(default=True)),
                ('length', models.IntegerField(help_text='Duration of the slot in minutes')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='availability_slots', to='proxy.school')),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
    ]
