import json

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from tracker.forms import SearchForm
from tracker.models import Show
from tracker.serializers import ShowSerializer
from tracker.shows_db.show_lookup import TvShows
from user_auth.models import User

from django.views import View
from django.views.generic import FormView, ListView


# Create your views here.
class ShowsList(APIView):
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def get(self, request):
        name = request.query_params.get("name")
        if name and len(name) < 3:
            return Response(data={"Size of the name param should be at least 3 characters long"},
                            status=status.HTTP_400_BAD_REQUEST)
        queryset = Show.objects.filter(Q(show_name__icontains=name))
        serializer = ShowSerializer(queryset, many=True)

        return Response(serializer.data)


class Home(FormView):
    template_name = "tracker/index.html"
    form_class = SearchForm


class SearchResults(ListView):
    template_name = "tracker/show_list.html"
    paginate_by = 10
    context_object_name = "results"

    def get_queryset(self):
        term = self.request.GET.get("q").strip()
        vector = SearchVector("show_name")
        query = SearchQuery(term)
        shows = Show.objects.annotate(rank=SearchRank(vector, query)).filter(Q(show_name__icontains=term)).order_by(
            "-rank")
        if not shows.exists():
            shows_lookup = TvShows(term)
            results = shows_lookup.db_save()
        else:
            results = []
            for show in shows:
                added = False
                try:
                    added = bool(show.users.get(id=self.request.user.id))
                except User.DoesNotExist:
                    pass
                results.append(
                    dict(added=added, show_id=show.show_id, show_name=show.show_name, picture_url=show.picture_url,
                         service=show.service, kind=show.kind, overview=show.overview, year=show.year))
        return results


class ChangeShowList(View):

    def post(self, request, pk):
        data = json.loads(request.body.decode("utf-8"))
        term = data["alter_show_list"]
        show = Show.objects.get(pk=pk)
        if term == "add":
            request.user.shows.add(show)
        elif term == "remove":
            request.user.shows.remove(show)

        return HttpResponse(200)


class Watchlist(ListView):
    # add login required decorator
    template_name = "tracker/show_list.html"
    paginate_by = 10
    context_object_name = "results"

    def get_queryset(self):
        user_watchlist = Show.objects.filter(users__in=[self.request.user.id]).order_by("-user_shows__date_added")
        data = []
        for show in user_watchlist:
            data.append(dict(added=True, show_id=show.show_id, show_name=show.show_name, picture_url=show.picture_url,
                             service=show.service, kind=show.kind, overview=show.overview, year=show.year))

        return data
