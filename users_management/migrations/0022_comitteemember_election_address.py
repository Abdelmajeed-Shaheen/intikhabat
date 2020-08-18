# Generated by Django 2.2.14 on 2020-08-18 04:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_electionaddress'),
        ('users_management', '0021_candidate_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='comitteemember',
            name='election_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.ElectionAddress'),
        ),
    ]
