# Generated by Django 2.2.14 on 2020-08-31 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comitteetask',
            name='title',
            field=models.CharField(default='يرجى تعيين عنوان المهمة', max_length=50),
        ),
        migrations.AlterField(
            model_name='comitteetask',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
