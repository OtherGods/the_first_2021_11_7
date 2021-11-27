# Generated by Django 3.2.9 on 2021-11-24 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0014_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='categoryss',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.category'),
        ),
        migrations.AddField(
            model_name='question',
            name='desc',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='title',
            field=models.CharField(max_length=10, null=True),
        ),
    ]