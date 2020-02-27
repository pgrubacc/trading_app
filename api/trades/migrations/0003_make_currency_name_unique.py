# Generated by Django 2.2.10 on 2020-02-27 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trades', '0002_added_verbose_names_to_trades'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='name',
            field=models.CharField(max_length=12, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='currency',
            unique_together=set(),
        ),
    ]
