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
    template = 'tracker/search_results.html'
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
                print('exception')
            print(added)
            results.append({"added": added, "show_id": show.show_id, "show_name": show.show_name, "picture_url": show.picture_url,
                            "service": show.service})

    context = {
        'results': results,
    }
    return render(request, template, context)


def change_show_list(request, pk):
    print(pk)
    term = request.POST.get('alter_show_list')
    print(term)
    show = Show.objects.get(pk=pk)
    if term == 'add':
        print('bruh')
        request.user.shows.add(show)
    elif term == 'remove':
        print('no bruh')
        request.user.shows.remove(show)

    return HttpResponse()
# def search_results(request):


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('index')
#     else:
#         form = UserCreationForm()
#
#     context = {'form': form}
#     return render(request, 'account/register.html', context)
