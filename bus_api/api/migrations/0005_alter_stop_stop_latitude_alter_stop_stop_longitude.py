# Generated by Django 4.2.5 on 2023-09-16 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_alter_stop_stop_latitude_alter_stop_stop_longitude"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stop",
            name="stop_latitude",
            field=models.CharField(default=0, max_length=36),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="stop",
            name="stop_longitude",
            field=models.CharField(default="0", max_length=36),
            preserve_default=False,
        ),
    ]
