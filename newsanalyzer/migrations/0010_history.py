# Generated by Django 3.2.5 on 2021-08-24 00:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsanalyzer', '0009_auto_20210815_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, null=True)),
                ('date', models.CharField(max_length=255, null=True)),
                ('word_count', models.IntegerField(null=True)),
                ('positivity_index', models.IntegerField(null=True)),
                ('num_articles', models.IntegerField(null=True)),
            ],
        ),
    ]
