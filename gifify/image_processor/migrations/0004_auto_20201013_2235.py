# Generated by Django 3.1.1 on 2020-10-13 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_processor', '0003_auto_20201013_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='optional_text',
            field=models.CharField(default='PLACEHOLDER', max_length=50),
        ),
    ]