class Model():
    """
    基类, 用来显示类的信息
    """
    def __repr__(self):
        name = self.__class__.__name__
        properties = ('{}=({})'.format(k, v) for k, v in self.__dict__.items())
        s = '\n<{} \n  {}>'.format(name, '\n  '.join(properties))
        return s


class Task(Model):
    """
    存储任务信息
    """
    def __init__(self):
        self.id = 0
        self.title = ''
        self.url = ''
        self.file_name = ''
        self.file_url = ''
        self.is_download = False