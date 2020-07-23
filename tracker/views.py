from django.shortcuts import render, redirect
from django.http import HttpResponse
from tracker.models import Show
from user_auth.models import User
from tracker.shows_db.show_lookup import TvShows
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from tracker.forms import SearchForm


# Create your views here.

def index(request):
    template = 'tracker/index.html'
    context = {}
    form = SearchForm(request.GET)
    context['search_form'] = form
    return render(request, template, context)


def search_results(request):
    template = 'tracker/show_list.html'
    term = request.GET.get('q')

    vector = SearchVector('show_name')
    query = SearchQuery(term)
    print(query)
    print(vector)
    shows = Show.objects.annotate(rank=SearchRank(vector, query)).filter(Q(show_name__icontains=term)).order_by('-rank')
    print(shows)
    print(request.user.username)
    if not shows.exists():
        shows_lookup = TvShows(term)
        results = shows_lookup.db_save()
    else:
        results = []
        for show in shows:
            added = False
            try:
                added = bool(show.users.get(id=request.user.id))
            except User.DoesNotExist:
                pass
            results.append(
                {"added": added, "show_id": show.show_id, "show_name": show.show_name, "picture_url": show.picture_url,
                 "service": show.service})

    context = {
        'results': results,
    }
    return render(request, template, context)


def change_show_list(request, pk):
    term = request.POST.get('alter_show_list')
    show = Show.objects.get(pk=pk)
    if term == 'add':
        request.user.shows.add(show)
    elif term == 'remove':
        request.user.shows.remove(show)

    return HttpResponse()


def watchlist(request):
    template = 'tracker/show_list.html'
    user_watchlist = Show.objects.filter(users__in=[request.user.id]).order_by('-user_shows__date_added')
    results = []
    for show in user_watchlist:
        results.append(
            {"added": True, "show_id": show.show_id, "show_name": show.show_name, "picture_url": show.picture_url,
             "service": show.service})
    context = {
        'results': results
    }


    return render(request, template, context)
