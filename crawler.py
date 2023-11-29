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

if __name__ == "__main__":
    movies = MovieDataset()
    mv_json = movies.get_movies()
    for mv in mv_json:
        print(mv.get('huhu'))
        print(json.dumps(mv, indent=2))
        break