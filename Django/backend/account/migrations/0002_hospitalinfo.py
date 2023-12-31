# Generated by Django 3.2.7 on 2021-10-21 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HospitalInfo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('hname', models.CharField(max_length=50)),
                ('hcode', models.CharField(max_length=20)),
                ('hpost', models.CharField(max_length=50)),
                ('haddress', models.CharField(max_length=100)),
                ('hphone', models.CharField(blank=True, max_length=20, null=True)),
                ('hurl', models.CharField(blank=True, max_length=50, null=True)),
                ('hlng', models.FloatField()),
                ('hlat', models.FloatField()),
            ],
        ),
    ]
