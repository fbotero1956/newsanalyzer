# Generated by Django 3.2.5 on 2021-08-11 02:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsanalyzer', '0004_article_record_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateTimeField(null=True),
        ),
    ]
