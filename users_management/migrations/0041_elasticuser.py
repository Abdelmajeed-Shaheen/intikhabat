# Generated by Django 2.2.14 on 2020-09-13 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_management', '0040_auto_20200910_1056'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElasticUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elector_no', models.IntegerField()),
                ('elector_name', models.CharField(max_length=255)),
                ('circle_name', models.CharField(max_length=255)),
                ('election_place_name', models.CharField(max_length=255)),
            ],
        ),
    ]
