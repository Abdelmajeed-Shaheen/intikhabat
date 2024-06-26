# Generated by Django 2.2.14 on 2020-09-02 10:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_management', '0034_auto_20200902_1157'),
        ('tasks', '0002_auto_20200831_1317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_body', models.CharField(max_length=500)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.ComitteeTask')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users_management.UserProfile')),
            ],
        ),
    ]
