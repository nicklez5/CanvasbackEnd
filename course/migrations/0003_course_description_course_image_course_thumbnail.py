# Generated by Django 5.2.1 on 2025-06-03 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='course_images/'),
        ),
        migrations.AddField(
            model_name='course',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='course_images/thumbnails/'),
        ),
    ]
