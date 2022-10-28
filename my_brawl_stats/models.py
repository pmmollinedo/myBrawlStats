from django.db import models


class Brawler(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class StarPower(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    brawler = models.ForeignKey(Brawler, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Gadget(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    brawler = models.ForeignKey(Brawler, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Player(models.Model):
    tag = models.CharField(verbose_name="Player tag identificator.",max_length=20,primary_key=True)
    name = models.CharField(verbose_name="Player name.",max_length=50)
    name_color = models.CharField("Name HEX code color.",max_length=50)
    icon = models.CharField("Player icon id.", max_length=50)
    trophies = models.IntegerField("Player actual trophies.", default=0)
    highest_trophies = models.IntegerField(default=0)
    highest_power_play_points = models.IntegerField(default=0)
    exp_level = models.IntegerField("Experience level.", default=0)
    exp_points = models.IntegerField("Experience points.", default=0)
    is_qualified = models.BooleanField("Qualified from championship challenge", default=False)
    solo_victories = models.IntegerField("Singleplayer total victories.", default=0)
    duo_victories = models.IntegerField("Duo total victories.", default=0)
    normal_victories = models.IntegerField("3vs3 total victories.", default=0)
    best_time_robo_rumble = models.IntegerField("Best time in Robo Rumble game mode.", default=0)
    best_time_big_brawler = models.IntegerField("Best time in Big Brawler game mode.", default=0)
    club_tag = models.CharField("Club tag identificator.", max_length=20)
    club_name = models.CharField("Club name.", max_length=20)
    brawlers = models.ManyToManyField(Brawler, through='UnlockedBrawler')

    def __str__(self):
        return self.name


class UnlockedBrawler(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    brawler = models.ForeignKey(Brawler, on_delete=models.CASCADE)
    highestTrophies = models.IntegerField(default=0)
    gadgets = models.ManyToManyField(Gadget)
    starpowers = models.ManyToManyField(StarPower)

    class Meta:
        unique_together = [['player', 'brawler']]

    def __str__(self):
        return self.brawler.name


class BrawlerStat(models.Model):
    unlocked_brawler = models.ForeignKey(
        UnlockedBrawler, on_delete=models.CASCADE)
    date = models.DateTimeField()
    power = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    trophies = models.IntegerField(default=0)

    class Meta:
        unique_together = [['date', 'unlocked_brawler']]
    
    def __str__(self):
        return self.unlocked_brawler.brawler.name
