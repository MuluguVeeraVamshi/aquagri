# Generated by Django 4.0.3 on 2022-03-31 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_cart_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
