# Generated by Django 4.0.3 on 2022-03-30 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_cart_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
