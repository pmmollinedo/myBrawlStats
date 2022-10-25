from django.db import models

class Player(models.Model):
    tag = models.CharField("Player tag identificator.", max_length=20, primary_key=True)
    name = models.CharField("Player name.", max_length=50)
    name_color = models.CharField("Player's name color HEX code.", max_length=50)
    icon = models.CharField("Player icon id.", max_length=50)
    trophies = models.IntegerField("Player actual trophies.", default=0)
    highest_trophies = models.IntegerField(default=0)
    highest_power_play_points = models.IntegerField(default=0)
    exp_level = models.IntegerField("Experience level.", default=0)
    exp_points = models.IntegerField("Experience points.", default=0)
    is_qualified_from_championship_challenge = models.BooleanField(default=False)
    solo_victories = models.IntegerField("Singleplayer total victories.", default=0)
    duo_victories = models.IntegerField("Duo total victories.", default=0)
    normal_victories = models.IntegerField("3vs3 total victories.", default=0)
    best_time_robo_rumble = models.IntegerField("Best time in Robo Rumble game mode.", default=0)
    best_time_big_brawler = models.IntegerField("Best time in Big Brawler game mode.", default=0)
    club_tag = models.CharField("Club tag identificator.", max_length=20)
    club_name = models.CharField("Club name.",max_length=20)

    def __str__(self):
        return self.name

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

class BrawlersHistory(models.Model):
    date = models.DateTimeField()
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    brawler = models.ForeignKey(Brawler, on_delete=models.CASCADE)
    power = models.IntegerField(default=0)
    rank = models.IntegerField(default=0)
    trophies = models.IntegerField(default=0)
    highestTrophies = models.IntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'brawler', 'player'], name='unique_date_brawler_player_constraint'
            )
        ]
    
    def __str__(self):
        return self.brawler.name

class UnlockedGadget(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    brawler = models.ForeignKey(Brawler, on_delete=models.CASCADE)
    gadget = models.ForeignKey(Gadget, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['player', 'brawler', 'gadget'], name='unique_player_brawler_gadget_constraint'
            )
        ]
    
    def __str__(self):
        return self.gadget.name

class UnlockedStarPower(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    brawler = models.ForeignKey(Brawler, on_delete=models.CASCADE)
    star_power = models.ForeignKey(StarPower, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['player', 'brawler', 'star_power'], name='unique_player_brawler_starpower_constraint'
            )
        ]
    
    def __str__(self):
        return self.star_power.name