# Generated by Django 4.2.5 on 2023-10-02 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quoteapp', '0003_alter_quote_quote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='born_date',
            field=models.DateField(),
        ),
    ]
