import requests

class Coursera(object):
    @staticmethod
    def search_courses(query=None):
        url = 'https://api.coursera.org/api/courses.v1'

        params = {
            'q': 'search',
            'query': query
        }

        r = requests.get(url, params=params)

        return r.json()
