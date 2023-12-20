import os, sys
sys.path.append('../')
from app import crawler
import json

# 10000 movies
def append_to_json(data, file_path):
    cnt = 0
    # print(data)
    for mv in data:
        cnt +=1
        with open(file_path, 'a', encoding='utf-8') as jsonl_file:
            jsonl_file.write(json.dumps(mv, ensure_ascii=False, indent=2) + ',\n')
    return cnt

if __name__ == "__main__":
    movies = crawler.MovieDB()
    path = 'movies_data.jsonl'
    cnt = 0
    for i in range(0):
        mv_json = movies.get_movies(page=i+1)
        cnt += append_to_json(data=mv_json, file_path=path)
        print(f'{i+1}: got {cnt} movies')
        
        