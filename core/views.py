from logging import debug, error as log_error

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from core.models import Tournament, Player, Match

def home(request, tournament=None):
    if tournament:
        tournament = Tournament.objects.filter(name=tournament)
    if tournament:
        tournament = tournament[0]
    else:
        tournament = Tournament.objects.get_current()

    error = request.GET.get('error')

    debug('Error = %s' % bool(error))

    return render(request, 'home.html', {'tournament': tournament, 'error': error})

def timetable(request):
    debug(request.__dict__)
    license = request.GET.get('license')
    tournament_id = request.GET.get('tid')

    if tournament_id:
        tournament = Tournament.objects.get(id=tournament_id)
    else:
        str_error = '------There is no tournament on the request ------\n'
        log_error(str_error + str(request.__dict__))
        raise Exception(str_error)

    player = None

    if license:
        player = Player.objects.filter(license=license)

    if license and player:
        player = Player.objects.get(license=license)
        debug(Match.objects.all())
        matches = list(Match.objects.filter(player1=player,
                    tournament=tournament))
        matches = matches + list(Match.objects.filter(player2=player,
                    tournament=tournament))
        matches.sort(key=lambda x: x.match_time)
        for p in matches:
            if p.player1 == player:
                p.player1_saw_timetable = True
            elif p.player2 == player:
                p.player2_saw_timetable = True
            elif p.player3 == player:
                p.player3_saw_timetable = True
            elif p.player4 == player:
                p.player4_saw_timetable = True
            p.save()

        template = ''

        if request.is_ajax():
            template = 'includes/timetable.html'
        else:
            template = 'timetable.html'

        return render(request, template, {'player': player,
            'matches': matches, 'tournament': tournament})
    elif request.is_ajax():
        return render(request, 'includes/error.html')
    else:
        return redirect(reverse('home', kwargs={'tournament':tournament.name}) + '?error=True')

@login_required
def match_list(request, tournament_id=None):
    if tournament_id:
        tournament = Tournament.objects.filter(id=tournament_id)[0]
    else:
        tournament = Tournament.objects.get_current()
        tournament_id = tournament.id

    categories = tournament.get_categories_list()

    full_list = []
    for category in categories:
        matches = category.matches.filter(tournament__id=tournament_id)
        match_list = []
        for match in matches:
            match_list.append({'match': match,
                'saw1':match.player1_saw_timetable,
                'saw2': match.player2_saw_timetable})

        full_list.append({'category': category,
            'matches': match_list})


    return render(request, 'match_list.html',
            {'full_list': full_list, 'tournament': tournament})

