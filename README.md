### 主从分布式爬虫

+ 采用Redis为任务队列服务
+ 主程序获取任务
+ 从程序获得数据并下载
+ 通过代理接口获取数据

### 本地环境配置
+ 安装python3和Redis
+ 安装requests与Redis相关的库
+ 克隆项目到本地
```
git clone https://github.com/zhourunliang/master-slave-crawler
```
+ 修改config.py
+ 运行主爬虫
```
python master.py
```
+ 运行从爬虫
```
python salver.py
```
### 设计图
![示例](https://github.com/zhourunliang/master-slave-crawler/blob/master/images/主从分布式爬虫.png)