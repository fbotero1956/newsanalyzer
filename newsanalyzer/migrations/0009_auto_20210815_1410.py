# Generated by Django 3.2.5 on 2021-08-15 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsanalyzer', '0008_article_num_articles'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='avg_word_length',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='common_words_1',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='common_words_2',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='common_words_3',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='common_words_4',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='common_words_5',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='common_words_tally_1',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='common_words_tally_2',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='common_words_tally_3',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='common_words_tally_4',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='common_words_tally_5',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='distinct_word_count',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='neg_tally',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='pos_tally',
            field=models.IntegerField(null=True),
        ),
    ]
