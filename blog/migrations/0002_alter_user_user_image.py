# Generated by Django 4.2.3 on 2023-09-20 09:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="user_image",
            field=models.ImageField(
                default="default_image.png", upload_to="user_images/"
            ),
        ),
    ]
