# Generated by Django 2.2 on 2020-05-31 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_blogpost_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='slug',
            field=models.SlugField(default='hey'),
            preserve_default=False,
        ),
    ]
