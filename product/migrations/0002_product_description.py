# Generated by Django 4.0.4 on 2022-06-14 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.CharField(default='no description', max_length=100),
        ),
    ]
