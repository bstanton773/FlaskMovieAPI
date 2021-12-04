import httpx

class MovieRankings():
    def __init__(self):
        self.base_url = "https://tmrdb.tmrdb.com/reviews/"
        self.base_header = {
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://www.movierankings.net'
        }
        self.search_header = {
            'accept': 'application/json, text/plain, */*',
            'awards': '',
            'characters': '',
            'country': '',
            'decades': '',
            'directors': '',
            'genres': '',
            'origin': 'https://www.movierankings.net',
            'page': '1',
            'providers': '',
            'ratingrange': '0@100',
            'ratings': 'avg',
            'runtime': '242',
            'skip': '0',
            'sort': 'rating@ASC',
            'sportholidays': '',
            'studiocompanies': '',
            'subgenres': '',
            'type': '',
            'universes': '',
            'years': ''
        }
        self.providers = {
            '': '',
            'Amazon Prime': '9', 
            'Disney+': '337', 
            'HBO Max': '384', 
            'Hulu': '15', 
            'Netflix': '8', 
            'Paramount+': '531', 
            'Peacock': '386', 
            'Peacock Premium': '387', 
            'Showtime': '37', 
            'Starz': '43'
        }
        
    def _get(self, url, headers={}):
        response = httpx.get(url, headers=headers)
        return response

    def get_movie_info(self, movie_id):
        url = self.base_url + "movie/" + str(movie_id)
        headers = self.base_header
        res = self._get(url, headers)
        if res.status_code == 200:
            return res.json()
        return res
    
    def search_filters(self, **kwargs):
        url = self.base_url + "all"
        headers = self.search_header.copy()
        for key, value in kwargs.items():
            headers[key] = str(value)
        res = self._get(url, headers)
        if res.status_code == 200:
            return res.json()


    def search_all(self, q='', **kwargs):
        url = self.base_url + f"search/?query={q}"
        headers = self.search_header.copy()
        for key, value in kwargs.items():
            headers[key] = str(value)
        if kwargs['providers']:
            headers['providers'] = '@'.join([self.providers[p] for p in kwargs['providers']])
        if kwargs['genres']:
            headers['genres'] = '@'.join([str(g) for g in kwargs['genres']])
        if kwargs['years']:
            headers['years'] = '@'.join([str(y) for y in kwargs['years']])
        res = self._get(url, headers)
        if res.status_code == 200:
            return res.json()