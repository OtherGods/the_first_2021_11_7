# Generated by Django 3.2.9 on 2021-11-08 11:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_category_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': '分类'},
        ),
    ]
