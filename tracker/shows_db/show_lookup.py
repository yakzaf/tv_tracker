import requests
from decouple import config
from tracker.models import Show
from django.conf import settings


def image_save(show_name, pic_url):
    request = requests.get(pic_url, stream=True)
    if request.status_code != requests.codes.ok:
        return
    path = settings.MEDIA_ROOT + f'{show_name}.webp'
    print(path)
    with open(path, 'wb') as f:
        for block in request.iter_content(1024 * 1024 * 10):
            if not block:
                break
            f.write(block)
    return f'{show_name}.webp'



class TvShows:
    def __init__(self, term):
        self.term = term

    def db_save(self):
        url = "https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/lookup"
        params = {'term': self.term.replace(' ', '-').lower()}
        headers = {
            'x-rapidapi-host': "utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com",
            'x-rapidapi-key': config('UTELLY_API_KEY')
        }
        try:
            r = requests.get(url, headers=headers, params=params)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        response_json = r.json()
        if len(response_json["results"]) == 0:
            return
        results = []
        item_list = []
        for result in response_json["results"]:
            show_name = result["name"]
            request_services = result["locations"]
            pic = result["picture"]
            picture_path = f'/media/{image_save(show_name, pic)}'
            services = []
            for s in request_services:
                services.append(s["display_name"])

            # item = Show(show_name=show_name, picture_url=picture_path, service=services)
            # item.save()
            item = {"show_name": show_name, "picture_url": picture_path, "service": services}
            item_list.append(Show(**item))

        Show.objects.bulk_create(item_list)
        results = [{"show_id": item_list[i].show_id, "show_name": item_list[i].show_name,
                    "picture_url": item_list[i].picture_url, "service": item_list[i].service} for i in
                   range(len(item_list))]

        return results
