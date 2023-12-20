import requests
import json

# get momives only, not tv series or others

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
            "vote_count.gte": 0,
        }
        response = requests.get(url_movies, headers=self.headers, params=querystring)
        movies_list = response.json()["results"]
        res = []
        for movie in movies_list:
            url_detail = self.url + f"/movie/{movie['id']}"
            query_detail= {
                "language": "en-US"
            }
            response = requests.get(url_detail, headers=self.headers, params=query_detail)
            res.append(response.json())
        return res


if __name__ == "__main__":
    movies = MovieDB()
    mv_json = movies.get_movies(page=191)
    print(json.dumps( mv_json, indent=2))
    # for mv in mv_json:
    #     # print(mv.get('ratingsSummary'))
    #     print(json.dumps(mv, indent=2))