import requests
from decouple import config
from tracker.models import Show
from django.conf import settings
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q


def image_save(show_name, pic_url):
    if pic_url is None:
        return
    try:
        request = requests.get(pic_url, stream=True)
    except requests.HTTPError:
        return
    path = settings.MEDIA_ROOT + f'{show_name}.png'
    print(path)
    with open(path, 'wb') as f:
        for block in request.iter_content(1024 * 1024 * 10):
            if not block:
                break
            f.write(block)
    return f'{show_name}.png'


class TvShows:
    def __init__(self, term):
        self.term = term

    def db_save(self):
        omdb_url = "http://www.omdbapi.com/"
        utelly_url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"
        params = {'term': self.term.replace(' ', '-').lower()}
        headers = {
            'x-rapidapi-host': "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com",
            'x-rapidapi-key': config('UTELLY_API_KEY')
        }

        try:
            r = requests.get(utelly_url, headers=headers, params=params)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        utelly_r_json = r.json()
        print(f'length = {len(utelly_r_json["results"])}')

        if len(utelly_r_json["results"]) == 0:
            return
        results = []
        item_list = []
        for result in utelly_r_json["results"]:
            show_name = result["name"]
            params = {'t': show_name, 'plot': 'short', 'apikey': config('OMDB_API_KEY')}
            try:
                r = requests.get(omdb_url, params=params)
                r.raise_for_status()
            except requests.exceptions.HTTPError as err:
                raise SystemExit(err)
            omdb_r_json = r.json()
            print(omdb_r_json)
            year = omdb_r_json["Year"]
            overview = omdb_r_json["Plot"]
            kind = omdb_r_json["Type"].capitalize()
            shows = Show.objects.filter(show_name__exact=show_name)
            if shows.exists():
                results.append(
                    dict(show_id=shows[0].show_id, show_name=shows[0].show_name, picture_url=shows[0].picture_url,
                         year=year, kind=kind, overview=overview, service=shows[0].service))
                continue
            request_services = result["locations"]
            pic = result["picture"]
            picture_path = f'/media/{image_save(show_name, pic)}'
            services = []
            for s in request_services:
                services.append(s["display_name"])

            item = dict(show_name=show_name, picture_url=picture_path, year=year, kind=kind, overview=overview,
                        service=services)
            item_list.append(Show(**item))

        if item_list:
            Show.objects.bulk_create(item_list)
            results = [dict(show_id=item_list[i].show_id, show_name=item_list[i].show_name,
                            picture_url=item_list[i].picture_url, year=item_list[i].year, kind=item_list[i].kind,
                            overview=item_list[i].overview, service=item_list[i].service) for i in range(len(item_list))]

        return results
