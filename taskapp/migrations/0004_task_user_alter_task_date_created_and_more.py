# Generated by Django 5.0 on 2024-01-05 03:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskapp', '0003_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='taskapp.user'),
        ),
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(default='null', max_length=300),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('in_progress', 'In Progress'), ('pending', 'Pending'), ('completed', 'Completed')], max_length=20),
        ),
        migrations.AlterField(
            model_name='task',
            name='title',
            field=models.CharField(default='null', max_length=100),
        ),
    ]
