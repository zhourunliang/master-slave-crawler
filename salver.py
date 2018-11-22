import os
import requests
from pyquery import PyQuery as pq
import re
import json

import config
from cache import RedisCache


def get_page(url):
    '''
    获取页面
    '''
    proxies = config.proxies
    try:
        res = requests.get(url,proxies=proxies)
        # print(res.text)
    except requests.exceptions.ConnectionError as e:
        print('Error',e.args)
    page = res.content
    return page


def begin_task(task_id, file_name, file_url):
    print('begin task {}'.format(task_id))
    redis_cache = RedisCache()
    # 添加到正在下载列表
    redis_cache.sadd('Task:begin', task_id)
    print('download...{}'.format(file_name))
    folder = config.down_folder
    path = os.path.join(folder, file_name)
    download(file_url, path)
    print('end task {}'.format(task_id))


def download(link, path):
    redis_cache = RedisCache()
    proxies = config.proxies
    if os.path.exists(path):
        print('file exist')
    else:
        try:
            r = requests.get(link,proxies=proxies,stream=True)
            total_length = int(r.headers['Content-Length'])
            with open(path, "wb") as code:
                code.write(r.content)
                # 文件是否完整
                length = os.path.getsize(path)
                print('length={}'.format(length))
                print('total_length={}'.format(total_length))
                if  total_length != length:
                    # 删除旧文件
                    os.remove(path)
                    # 重新下载
                    download(path, link)
                else:
                    print('download success')
                    # 添加到已下载
                    file_name = os.path.basename(path)
                    content_id = file_name[:5]
                    redis_cache.srem('Task:begin', content_id)
                    redis_cache.sadd('Task:finish', content_id)
            # print(r.text)
        except requests.exceptions.ConnectionError as e:
            print('Error',e.args)


def main():
    redis_cache = RedisCache()
    #  检查任务列表是否在已下载列表中
    keys = redis_cache.keys('Task:id:[0-9]*')
    # print(keys)
    new_key = [key.decode() for key in keys]
    # print(new_key)
    # 按id排序
    new_key = sorted(new_key,key = lambda i:int(i.split(':')[2]))
    # print(new_key)
    for key in new_key:
        task_id = key.split(':')[2]
        # print(task_id)
        is_finish = redis_cache.sismember('Task:finish', task_id)
        is_begin = redis_cache.sismember('Task:begin', task_id)
        if is_finish==1:
            print('Task {} is finish'.format(task_id))
        elif is_begin==1:
            print('Task {} is begin'.format(task_id))
        else:
            file_name = json.loads(redis_cache.get(key).decode('utf-8').replace("\'", "\""))['file_name']
            file_url = json.loads(redis_cache.get(key).decode('utf-8').replace("\'", "\""))['file_url']
            # print(file_url)
            begin_task(task_id, file_name, file_url)

if __name__ == '__main__':
    main()

