# Generated by Django 3.2.5 on 2021-09-03 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsanalyzer', '0010_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='Single_history',
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
