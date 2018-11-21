import os
import requests
from pyquery import PyQuery as pq
import re
import json

import config
from cache import RedisCache
from model import Task


def parse_link(div):
    '''
    获取连接
    '''
    e = pq(div)
    href = e.find('a').attr('href')
    return href

def get_from_url(url):
    '''
    获取列表连接
    '''
    page = get_page(url)
    e = pq(page)
    items = e('.epiItem.video')
    links = [parse_link(i) for i in items]
    print(len(links))
    links.reverse()
    return links

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

def get_all_file(path, fileList=[]):
    '''
    获取目录下所有文件
    '''
    get_dir = os.listdir(path)  #遍历当前目录，获取文件列表
    for i in get_dir:
        sub_dir = os.path.join(path,i)  # 把第一步获取的文件加入路径
        # print(sub_dir)
        if os.path.isdir(sub_dir):     #如果当前仍然是文件夹，递归调用
            get_all_file(sub_dir, fileList)
        else:
            ax = os.path.abspath(sub_dir)  #如果当前路径不是文件夹，则把文件名放入列表
            # print(ax)
            fileList.append(ax)
    return fileList

def init_finish_task(path):
    '''
    初始化已结束任务
    '''
    redis_cache = RedisCache()
    fileList = []
    fileList = get_all_file(path, fileList)
    # print(fileList)
    for file in fileList:
        file_name = os.path.basename(file)
        task_id = file_name[:5]
        # print(task_id)
        redis_cache.sadd('Task:finish', task_id)
    print('init_finish_task...end')

def init_task_url():
    '''
    初始化已结束任务url
    '''
    redis_cache = RedisCache()
    url = config.list_url
    link_list = get_from_url(url)
    for link in link_list:
        task_url = config.task_url_head+link
        # print(task_url)
        task_id = task_url[-5:]
        # redis_cache.set('Task:id:{}:url'.format(task_id),task_url)
        t = task_from_url(task_url)
        print(t.__dict__)
        redis_cache.set('Task:id:{}'.format(task_id), t.__dict__)
        # print(t)        

def task_from_url(task_url):
    page = get_page(task_url)
    e = pq(page)

    task_id = task_url[-5:]
    title = e('.controlBar').find('.epi-title').text().replace('/', '-')
    file_url = e('.audioplayer').find('audio').attr('src')
    ext = file_url[-4:]
    file_name = task_id+'.'+title+ext

    t = Task()
    t.id = task_id
    t.title = title
    t.url = task_url
    t.file_name = file_name
    t.file_url =  file_url
    t.is_download = False
    return t

def main():
    init_task_url()
    init_finish_task(config.down_folder)

if __name__ == '__main__':
    main()

