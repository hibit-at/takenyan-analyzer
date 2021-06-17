# Generated by Django 3.1 on 2021-06-17 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tw_id', models.CharField(default='', max_length=280)),
                ('dt', models.DateTimeField()),
                ('usr', models.CharField(default='', max_length=280)),
                ('txt', models.CharField(default='', max_length=280)),
            ],
        ),
    ]
