# Generated by Django 3.2.5 on 2021-08-12 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsanalyzer', '0007_alter_article_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='num_articles',
            field=models.IntegerField(null=True),
        ),
    ]
