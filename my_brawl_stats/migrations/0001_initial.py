# Generated by Django 4.1.2 on 2022-10-28 14:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brawler',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Gadget',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('brawler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_brawl_stats.brawler')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('tag', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='Player tag identificator.')),
                ('name', models.CharField(max_length=50, verbose_name='Player name.')),
                ('name_color', models.CharField(max_length=50, verbose_name='Name HEX code color.')),
                ('icon', models.CharField(max_length=50, verbose_name='Player icon id.')),
                ('trophies', models.IntegerField(default=0, verbose_name='Player actual trophies.')),
                ('highest_trophies', models.IntegerField(default=0)),
                ('highest_power_play_points', models.IntegerField(default=0)),
                ('exp_level', models.IntegerField(default=0, verbose_name='Experience level.')),
                ('exp_points', models.IntegerField(default=0, verbose_name='Experience points.')),
                ('is_qualified', models.BooleanField(default=False, verbose_name='Qualified from championship challenge')),
                ('solo_victories', models.IntegerField(default=0, verbose_name='Singleplayer total victories.')),
                ('duo_victories', models.IntegerField(default=0, verbose_name='Duo total victories.')),
                ('normal_victories', models.IntegerField(default=0, verbose_name='3vs3 total victories.')),
                ('best_time_robo_rumble', models.IntegerField(default=0, verbose_name='Best time in Robo Rumble game mode.')),
                ('best_time_big_brawler', models.IntegerField(default=0, verbose_name='Best time in Big Brawler game mode.')),
                ('club_tag', models.CharField(max_length=20, verbose_name='Club tag identificator.')),
                ('club_name', models.CharField(max_length=20, verbose_name='Club name.')),
            ],
        ),
        migrations.CreateModel(
            name='StarPower',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=20)),
                ('brawler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_brawl_stats.brawler')),
            ],
        ),
        migrations.CreateModel(
            name='UnlockedBrawler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highestTrophies', models.IntegerField(default=0)),
                ('brawler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_brawl_stats.brawler')),
                ('gadgets', models.ManyToManyField(to='my_brawl_stats.gadget')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_brawl_stats.player')),
                ('starpowers', models.ManyToManyField(to='my_brawl_stats.starpower')),
            ],
            options={
                'unique_together': {('player', 'brawler')},
            },
        ),
        migrations.AddField(
            model_name='player',
            name='brawlers',
            field=models.ManyToManyField(through='my_brawl_stats.UnlockedBrawler', to='my_brawl_stats.brawler'),
        ),
        migrations.CreateModel(
            name='BrawlerStat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('power', models.IntegerField(default=0)),
                ('rank', models.IntegerField(default=0)),
                ('trophies', models.IntegerField(default=0)),
                ('unlocked_brawler', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='my_brawl_stats.unlockedbrawler')),
            ],
            options={
                'unique_together': {('date', 'unlocked_brawler')},
            },
        ),
    ]
