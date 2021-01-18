from weasyprint import HTML
import os
import time
from coordinate_sys.process_model import dbo
from coordinate_sys.extensions import root_path
from apscheduler.schedulers.blocking import BlockingScheduler

import threading
from queue import Queue


from collections import namedtuple
Name_tuple_st = namedtuple('Name_tuple_st', ['index', 'item'])


pre_url = r"http://127.0.0.1:5000/process/stations/"



station_list_all = dbo.read_table('station_view')['station'].to_list()
station_list = station_list_all
station_list_name_tuple = [Name_tuple_st(x[0], x[1]) for x in enumerate(station_list)]


def create_pdf():
    save_path = os.path.join(root_path, 'static\\download')
    save_name = 'stations.pdf'
    save_file = os.path.join(save_path, save_name)
    t1 = time.time()
    pages = []
    for station in station_list:
        url = pre_url + station
        html = HTML(url=url)
        pages.extend(html.render().pages)

    HTML(string="").render().copy(pages).write_pdf(save_file)

    td = time.time() - t1
    print(td)


def one_station_pages(station):
    pre_url = r"http://127.0.0.1:5000/process/stations/"    #todo: 待删除此列，改为类方法后
    url = pre_url + station
    html = HTML(url=url)
    page_list = html.render().pages
    return page_list


def print_everyday():
    scheduler = BlockingScheduler()
    scheduler.add_job(create_pdf, 'cron', hour=1, minute=11, second=11)
    scheduler.start()





class Worker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.q = queue
        self.thread_stop = False
        self.pages = []

    def run(self):
        while not self.thread_stop:
            print(f"thread {self.ident} {self.name}: waiting for task")
            try:
                task = self.q.get(block=True, timeout=20)   #接受任务
            except Exception:     #todo:待确认
                print("Nothing to do ,I will go home!")
                self.thread_stop = True
                break
            print(f"task index:{task[0]}, task item:{task[1]}")
            print("I am working")
            pg = one_station_pages(task[1])
            temp=Name_tuple_st(task[0], pg)
            self.pages.append(temp)
            print("working finished")
            self.q.task_done()      #todo: 待确认
            res = self.q.qsize()
            if res > 0:
                print(f"fuck ! There are still {res} tasks to do ")

    def stop(self):
        self.thread_stop = True


def temp():
    t1 = time.time()
    q = Queue(2)
    worker = Worker(q)

    worker.start()
    print("******** leader: wait for task put in finished! ")

    task_list = station_list_name_tuple[:5]
    for task in task_list:
        q.put(task, block=True, timeout=None)

    q.join()    #等待所有任务完成
    print("******** leader: all task finished! ")

    td = time.time() - t1
    print(f"spend time {td} seconds")

    return worker