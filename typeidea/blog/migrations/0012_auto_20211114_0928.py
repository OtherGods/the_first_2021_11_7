# Generated by Django 3.2 on 2021-11-14 01:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_bookmark_taggeditem'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Bookmark',
        ),
        migrations.DeleteModel(
            name='TaggedItem',
        ),
    ]