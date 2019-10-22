import requests
from lxml import etree


class MovieComing(object):
    def __init__(self, url=None, user_agent=None):
        self.url = url if url else "https://movie.douban.com/coming"
        self.headers = {
            "User-Agent": user_agent if user_agent else "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36"
        }

    def _request(self):
        try:
            res = requests.get(self.url, headers=self.headers)
            status = res.status_code
        except Exception as e:
            print("请求失败：", self.url)
            print("error:", e)
            return 0
        if 200 <= status < 300:
            return res.text
        else:
            return 1

    def _path_data(self):
        res = self._request()
        if type(res) == type(2):
            return "error"
        tr_list = etree.HTML(res).xpath("//table[@class='coming_list']/tbody/tr")
        movies = []
        for tr in tr_list:
            td_list = tr.xpath("./td")
            movie = dict(
                movie_time=td_list[0].xpath("./text()")[0].strip(),
                name=td_list[1].xpath("./a/text()")[0].strip(),
                type=td_list[2].xpath("./text()")[0].strip(),
                location=td_list[3].xpath("./text()")[0].strip(),
                movie_url=td_list[1].xpath("./a/@href")[0]
            )
            movies.append(movie)
        return movies

    def get_all_movies(self):
        return self._path_data()

    def find_movies(self, key_word):
        data = self._path_data()
        if data == "error":
            return data
        movies = []
        for movie in data:
            if movie['name'].find(key_word) >= 0:
                movies.append(movie)
        return movies


if __name__ == '__main__':
    coming = MovieComing()
    co = coming.find_movies("护宝")
    print(co)