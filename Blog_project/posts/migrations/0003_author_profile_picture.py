# Generated by Django 2.1.5 on 2019-04-21 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_remove_author_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='profile_picture',
            field=models.ImageField(default='asd', upload_to=''),
        ),
    ]
