# Generated by Django 4.1.7 on 2023-03-01 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_student_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='sponsor',
            name='type',
            field=models.CharField(blank=True, choices=[('Jismoniy shaxs', 'Jismoniy shaxs'), ('Yuridik shaxs', 'Yuridik shaxs')], max_length=255, null=True),
        ),
    ]