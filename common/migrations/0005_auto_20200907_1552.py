# Generated by Django 2.2.14 on 2020-09-07 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_electionaddress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('governorate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Governorate')),
            ],
        ),
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Area')),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.District')),
                ('governorate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Governorate')),
                ('sector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.Sector')),
            ],
        ),
        migrations.AddField(
            model_name='area',
            name='sector',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.Sector'),
        ),
    ]
