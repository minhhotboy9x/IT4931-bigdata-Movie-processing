import requests
import json

# get momives only, not tv series or others
class MovieDataset:
    # get each batch data
    def __init__(self) -> None:
        self.url = "https://moviesdatabase.p.rapidapi.com/titles"
        self.headers = {
            "X-RapidAPI-Key": "319eb3c08emsh9ab555d649259d8p1e1b18jsnbb66ad4f8d24",
            "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
        }
        self.genres = self.get_genres()

    def get_genres(self):
        url_genres = self.url + "/utils/genres"
        response = requests.get(url_genres, headers=self.headers)
        return response.json()['results']
    
    def get_movies(self, startYear=2000, endYear=2023, page=1):
        querystring = {"startYear": startYear,
                       "titleType": "movie",
                       "page": page,
                       "info": "base_info",
                       "endYear": endYear}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        return response.json()['results']
    
    # def get_main_actors(self, id)

class MovieDB:
    # get each batch data
    def __init__(self) -> None:
        self.url = "https://api.themoviedb.org/3"
        self.headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3M2ZkOTg0MmMzMTg2ZDY2OWMxNmEwNmIzYTdjODA2OCIsInN1YiI6IjY1M2IyMzFlMTA5Y2QwMDEyY2ZlMWU2NCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.5nkctErbJj6FNm__3T8rX1iFXSFw5Qasd3JOXqGOKYU"
        }
        # self.genres = self.get_genres()

    def get_actors(self, page=1):
        url_actors = self.url + f"/person/popular?page={page}"
        response = requests.get(url_actors, headers=self.headers)
        return response.json()['results']

    def get_genres(self):
        url_genres = self.url + f"/genre/movie/list?language=en"
        response = requests.get(url_genres, headers=self.headers)
        return response.json()["genres"]

    def get_movies(self, primary_release_date_gt="1975-04-30", page=1):
        url_movies = self.url + "/discover/movie?"
        querystring = {
            "include_adult": "true",
            "include_video": "false",
            "language": "en-US",
            "page": page,
            "primary_release_date.gte": primary_release_date_gt,
            "vote_count.gte": 1000,
        }
        response = requests.get(url_movies, headers=self.headers, params=querystring)
        return response.json()['results']


if __name__ == "__main__":
    movies = MovieDB()
    mv_json = movies.get_movies()

    for mv in mv_json:
        # print(mv.get('ratingsSummary'))
        print(json.dumps(mv, indent=2))