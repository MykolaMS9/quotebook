# Generated by Django 4.2.5 on 2023-10-04 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0005_alter_tag_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='quote',
            field=models.CharField(max_length=300, unique=True),
        ),
    ]
