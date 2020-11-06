from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from tracker.models import Show
from user_auth.models import User
from tracker.shows_db.show_lookup import TvShows
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from tracker.forms import SearchForm
import json


# Create your views here.

def index(request):
    template = 'tracker/index.html'
    context = {}
    form = SearchForm(request.GET)
    context['search_form'] = form
    return render(request, template, context)


def search_results(request):
    template = 'tracker/show_list.html'
    term = request.GET.get('q').strip()
    page = request.GET.get('page', 1)
    vector = SearchVector('show_name')
    query = SearchQuery(term)
    if query.value:
        shows = Show.objects.annotate(rank=SearchRank(vector, query)).filter(Q(show_name__icontains=term)).order_by(
            '-rank')
    else:
        shows = Show.objects.none()

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
                dict(added=added, show_id=show.show_id, show_name=show.show_name, picture_url=show.picture_url,
                     service=show.service, kind=show.kind, overview=show.overview, year=show.year))
        paginator = Paginator(results, 10)
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)

    context = {'results': results}

    return render(request, template, context)


def change_show_list(request, pk):
    data = json.loads(request.body.decode('utf-8'))
    term = data['alter_show_list']
    show = Show.objects.get(pk=pk)
    if term == 'add':
        request.user.shows.add(show)
    elif term == 'remove':
        request.user.shows.remove(show)

    return HttpResponse()


def watchlist(request):
    page = request.GET.get('page', 1)
    template = 'tracker/show_list.html'
    user_watchlist = Show.objects.filter(users__in=[request.user.id]).order_by('-user_shows__date_added')
    results = []
    for show in user_watchlist:
        print(show.overview)
        results.append(
            dict(added=True, show_id=show.show_id, show_name=show.show_name, picture_url=show.picture_url,
                 service=show.service, kind=show.kind, overview=show.overview, year=show.year))

    paginator = Paginator(results, 10)
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        results = paginator.page(1)
    except EmptyPage:
        results = paginator.page(paginator.num_pages)

    context = {'results': results}

    return render(request, template, context)
