# Generated by Django 2.2.14 on 2020-08-27 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_management', '0029_candidate_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignadminstrator',
            name='candidate',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users_management.Candidate'),
        ),
    ]
