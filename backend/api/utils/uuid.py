import ulid
import datetime
import threading


def generate_db_id():
    # https://web.archive.org/web/20201129230946/https://www.percona.com/blog/2014/12/19/store-uuid-optimized-way/
    # https://zhuanlan.zhihu.com/p/592152224
    return str(ulid.ulid())


class CurrentCount(object):

    def __init__(self):
        self.prev_current = None
        self.count = 1000
        self.lock = threading.Lock()

    def get_current_count(self, current):
        self.lock.acquire()
        try:
            if self.prev_current == current:
                self.count = self.count + 1
            else:
                self.count = 1000
                self.prev_current = current
            return self.count
        finally:
            self.lock.release()


current_count = CurrentCount()


def generate_db_trade_no():
    # 交易流水号，每秒钟的时间计数
    now = datetime.datetime.now(datetime.UTC)
    current = now.strftime("%Y%m%d%H%M%S")
    count = current_count.get_current_count(current)
    return "%s%s" % (now, count)
