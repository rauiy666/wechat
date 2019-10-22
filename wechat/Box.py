import json
import locale
import time

import requests


locale.setlocale(locale.LC_CTYPE, 'chinese')


class Box(object):
    def __init__(self, url=None):
        self.url = url if url else "http://piaofang.maoyan.com/second-box"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
            "Referer": "http://piaofang.maoyan.com/dashboar"
        }

    def _request(self):
        try:
            res = requests.get(self.url, headers=self.headers)
            status = res.status_code
        except Exception as e:
            print("获取数据失败：%s" % self.url)
            print("error:", e)
            return 0
        if 200 <= status < 300:
            return res
        else:
            return status

    def get_movies(self):
        res = self._request()
        if type(res) == type(2):
            print("数据获取失败！")
            return "error"
        else:
            content = json.loads(res.text)
            total_box = content['data']['totalBox']
            m_list = content['data']['list']
            server_time = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(content['data']['serverTimestamp'] / 1000))
            movies = {'total_box': total_box, 'server_time': server_time}
            movies_list = [movies, ]
            for movie in m_list:
                movie_map = dict(
                    name=movie['movieName'],
                    release_info=movie['releaseInfo'],
                    sum_box_info=movie['sumBoxInfo'],
                    box_info=movie['boxInfo'],
                    box_rate=movie['boxRate'],
                    show_info=movie['showInfo'],
                    show_rate=movie['showRate'],
                    avg_show_view=movie['avgShowView'],
                    avg_seat_view=movie['avgSeatView']
                )
                movies_list.append(movie_map)
            return movies_list

    def find_movies(self, movies_name):
        res = self._request()
        if type(res) == type(2):
            print("数据获取失败！")
            return "error"
        else:
            content = json.loads(res.text)
            m_list = content['data']['list']
            movie_list = []
            for movie in m_list:
                if movie['movieName'].find(movies_name) >= 0:
                    movie_map = dict(
                        name=movie['movieName'],
                        release_info=movie['releaseInfo'],
                        sum_box_info=movie['sumBoxInfo'],
                        box_info=movie['boxInfo'],
                        box_rate=movie['boxRate'],
                        show_info=movie['showInfo'],
                        show_rate=movie['showRate'],
                        avg_show_view=movie['avgShowView'],
                        avg_seat_view=movie['avgSeatView']
                    )
                    movie_list.append(movie_map)
            return movie_list

    def get_count_box(self):
        res = self._request()
        if type(res) == type(2):
            print("数据获取失败！")
            return "error"
        else:
            content = json.loads(res.text)
            print(content)
            total_box = content['data']['totalBox']
            server_time = time.strftime("%Y年%m月%d日 %H:%M:%S", time.localtime(content['data']['serverTimestamp'] / 1000))
            return {"total_box": total_box, "server_time": server_time}

    def get_online_movies(self):
        res = self._request()
        if type(res) == type(2):
            print("数据获取失败！")
            return "error"
        else:
            content = json.loads(res.text)
            m_list = content['data']['list']
            movies = []
            for movie in m_list:
                movies.append(movie['movieName'])
            return movies


if __name__ == '__main__':
    box = Box()
    print(box.find_movies("魔"))