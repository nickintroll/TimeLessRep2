# Generated by Django 3.0.4 on 2023-02-25 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.CharField(default=0, max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
