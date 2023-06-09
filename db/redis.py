import redis

from typing import List


class RedisClient:

    MAX_RECENT_DLS_LEN = 10
    DB_NAME = "recent_downloads"

    def __init__(self, host, port):
        self.__redis = redis.Redis(host=host, port=port)
        recent_downloads_undecoded = self.__redis.lrange(self.DB_NAME, 0, -1)
        self.recent_downloads = [recent_download.decode("utf-8") for recent_download in recent_downloads_undecoded]

    def __save_db(self):
        with self.__redis.pipeline() as pipe:
            pipe.delete(self.DB_NAME)
            pipe.rpush(self.DB_NAME, *self.recent_downloads)
            pipe.execute()

    @property
    def get_recent_downloads(self) -> List:
        return self.recent_downloads

    def add_recent_download(self, movie: str):

        if movie in self.recent_downloads:
            return False

        if len(self.recent_downloads) == self.MAX_RECENT_DLS_LEN:
            self.recent_downloads.pop()

        self.recent_downloads.insert(0, movie)

        self.__save_db()
        with self.__redis.pipeline() as pipe:
            pipe.delete(self.DB_NAME)
            pipe.rpush(self.DB_NAME, *self.recent_downloads)
            pipe.execute()

        return True


