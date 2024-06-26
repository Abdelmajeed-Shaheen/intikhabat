# Generated by Django 2.2.14 on 2020-08-31 13:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('adminstration', '0010_auto_20200828_1220'),
        ('users_management', '0032_auto_20200831_1311'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComitteeTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('notes', models.TextField()),
                ('is_complete', models.BooleanField()),
                ('comittee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminstration.Comittee')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_management.UserProfile')),
            ],
        ),
    ]
