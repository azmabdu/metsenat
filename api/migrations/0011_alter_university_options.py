# Generated by Django 4.1.7 on 2023-03-05 20:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_donation_options_alter_sponsor_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='university',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Universities'},
        ),
    ]
