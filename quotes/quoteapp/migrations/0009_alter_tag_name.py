# Generated by Django 4.2.5 on 2023-10-07 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0008_remove_author_user_quote_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(unique=True),
        ),
    ]