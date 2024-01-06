# Generated by Django 5.0 on 2024-01-04 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(default='null', max_length=100)),
                ('lastname', models.CharField(default='null', max_length=100)),
                ('phone', models.CharField(default='0000000000', max_length=10)),
                ('dob', models.CharField(default='00-00-0000', max_length=10)),
                ('college', models.CharField(default='null', max_length=200)),
                ('email', models.EmailField(default='null', max_length=254)),
                ('password', models.CharField(default='null', max_length=100)),
                ('coins', models.IntegerField(default=0)),
            ],
        ),
    ]
