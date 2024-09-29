# Generated by Django 5.1.1 on 2024-09-29 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_app', '0002_alter_burn_event_id_alter_burn_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='burn',
            name='amount',
            field=models.DecimalField(decimal_places=20, max_digits=50),
        ),
        migrations.AlterField(
            model_name='burn',
            name='amount0',
            field=models.DecimalField(decimal_places=20, max_digits=50),
        ),
        migrations.AlterField(
            model_name='burn',
            name='amount1',
            field=models.DecimalField(decimal_places=20, max_digits=50),
        ),
        migrations.AlterField(
            model_name='mint',
            name='amount',
            field=models.DecimalField(decimal_places=20, max_digits=50),
        ),
        migrations.AlterField(
            model_name='mint',
            name='amount0',
            field=models.DecimalField(decimal_places=20, max_digits=50),
        ),
        migrations.AlterField(
            model_name='mint',
            name='amount1',
            field=models.DecimalField(decimal_places=20, max_digits=50),
        ),
        migrations.AlterField(
            model_name='swap',
            name='amount0',
            field=models.DecimalField(decimal_places=20, max_digits=50),
        ),
        migrations.AlterField(
            model_name='swap',
            name='amount1',
            field=models.DecimalField(decimal_places=20, max_digits=50),
        ),
    ]
