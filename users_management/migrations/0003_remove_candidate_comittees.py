# Generated by Django 2.2.14 on 2020-07-31 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_management', '0002_campaignadminstrator_candidate_comitteemember_communicationofficer_voter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate',
            name='comittees',
        ),
    ]
