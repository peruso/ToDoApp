# Generated by Django 3.1.14 on 2023-03-26 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='status',
            field=models.CharField(choices=[('not-started', 'Not started'), ('in-progress', 'In progress'), ('completed', 'Completed')], default='not-started', max_length=20),
        ),
    ]
