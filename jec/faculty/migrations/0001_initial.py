# Generated by Django 3.1.2 on 2022-10-26 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department', models.CharField(max_length=400)),
                ('designation', models.CharField(choices=[('p', 'Professor'), ('ap', 'Asst Professor'), ('asp', 'Associate professor')], max_length=3)),
                ('name', models.CharField(max_length=200)),
                ('dob', models.DateField()),
                ('doa', models.DateField()),
                ('exp', models.IntegerField(default=0)),
                ('regular', models.BooleanField(default=True)),
            ],
        ),
    ]
