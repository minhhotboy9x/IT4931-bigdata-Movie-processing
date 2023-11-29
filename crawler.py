import requests

# get momives only, not tv series or others
class MovieDataset:
    # get each batch data
    def __init__(self) -> None:
        self.url = "https://moviesdatabase.p.rapidapi.com/titles"
        self.headers = {
            "X-RapidAPI-Key": "319eb3c08emsh9ab555d649259d8p1e1b18jsnbb66ad4f8d24",
            "X-RapidAPI-Host": "moviesdatabase.p.rapidapi.com"
        }
        self.genres = self.get_genres()['results']

    def get_genres(self):
        url = "https://moviesdatabase.p.rapidapi.com/titles/utils/genres"
        response = requests.get(url, headers=self.headers)
        return response.json()

if __name__ == "__main__":
    movies = MovieDataset()
    print(movies.genres)