# Generated by Django 5.1.1 on 2024-09-28 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EthUsdcOhlcv',
            fields=[
                ('timestamp', models.DateTimeField(primary_key=True, serialize=False)),
                ('open', models.DecimalField(decimal_places=8, max_digits=20)),
                ('high', models.DecimalField(decimal_places=8, max_digits=20)),
                ('low', models.DecimalField(decimal_places=8, max_digits=20)),
                ('close', models.DecimalField(decimal_places=8, max_digits=20)),
                ('volume', models.DecimalField(decimal_places=10, max_digits=30)),
            ],
            options={
                'db_table': 'ethusdcohlcv',
            },
        ),
        migrations.CreateModel(
            name='Burn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.TextField()),
                ('amount', models.TextField()),
                ('amount0', models.TextField()),
                ('amount1', models.TextField()),
                ('owner', models.TextField()),
                ('pool_id', models.TextField()),
                ('tickLower', models.IntegerField()),
                ('tickUpper', models.IntegerField()),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'burn',
                'unique_together': {('event_id', 'timestamp')},
            },
        ),
        migrations.CreateModel(
            name='Mint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.TextField()),
                ('amount', models.TextField()),
                ('amount0', models.TextField()),
                ('amount1', models.TextField()),
                ('owner', models.TextField()),
                ('pool_id', models.TextField()),
                ('sender', models.TextField()),
                ('tickLower', models.IntegerField()),
                ('tickUpper', models.IntegerField()),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'mint',
                'unique_together': {('event_id', 'timestamp')},
            },
        ),
        migrations.CreateModel(
            name='Swap',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.TextField()),
                ('amount0', models.TextField()),
                ('amount1', models.TextField()),
                ('pool_id', models.TextField()),
                ('recipient', models.TextField()),
                ('sender', models.TextField()),
                ('sqrtPriceX96', models.TextField()),
                ('tick', models.IntegerField()),
                ('timestamp', models.DateTimeField(db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'swap',
                'unique_together': {('event_id', 'timestamp')},
            },
        ),
    ]
