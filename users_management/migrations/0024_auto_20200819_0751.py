# Generated by Django 2.2.14 on 2020-08-19 07:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_management', '0023_comitteemember_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate',
            name='election_list',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adminstration.ElectionList'),
        ),
    ]
