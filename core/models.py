#-*- encoding: utf-8 -*-

from django.db import models

class TournamentManager(models.Manager):

    def get_current(self):
        result = Tournament.objects.filter(
                    active=True).order_by('-starting_date')
        if result:
            return result[0]
        else:
            return None


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __unicode__(self):
        return self.name

    def get_tournaments_list(self):
        tournaments = []
        elements = CategoryInTournament.objects.filter(category=self)
        for elem in elements:
            tournaments.append(elem.tournament)

        return tournaments


class Tournament(models.Model):
    name = models.CharField(max_length=20)
    starting_date = models.DateField()
    ending_date = models.DateField()
    image = models.URLField(blank=True, verify_exists=False, max_length=200)
    active = models.BooleanField(default=True)

    objects = TournamentManager()

    def __unicode__(self):
        return self.name

    def get_categories_list(self):
        categories = []
        elements = CategoryInTournament.objects.filter(tournament=self)
        for elem in elements:
            categories.append(elem.category)

        return categories



class CategoryInTournament(models.Model):
    category = models.ForeignKey(Category, related_name='rel_tournaments')
    tournament = models.ForeignKey(Tournament, related_name='rel_categories')

    def __unicode__(self):
        return self.category.name + ' in ' + self.tournament.name


class Player(models.Model):
    name = models.CharField(max_length=50)
    license = models.CharField(max_length=20)

    def __unicode__(self):
        return self.name


class Match(models.Model):
    player1 = models.ForeignKey(Player, related_name='matches1')
    player2 = models.ForeignKey(Player, related_name='matches2')
    player3 = models.ForeignKey(Player, related_name='matches3',
            blank=True, null=True)
    player4 = models.ForeignKey(Player, related_name='matches4',
            blank=True, null=True)
    match_time = models.DateTimeField()
    tournament = models.ForeignKey(Tournament, related_name='matches')
    category = models.ForeignKey(Category, default=0,
            related_name='matches')

    player1_saw_timetable = models.BooleanField(default=False)
    player2_saw_timetable = models.BooleanField(default=False)
    player3_saw_timetable = models.BooleanField(default=False)
    player4_saw_timetable = models.BooleanField(default=False)

    def __unicode__(self):
        return self.player1.name + ' vs ' + self.player2.name


