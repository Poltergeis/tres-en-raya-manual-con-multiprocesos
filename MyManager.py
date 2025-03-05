from multiprocessing.managers import BaseManager

class MyManager(BaseManager):
    @staticmethod
    def create_default():
        return MyManager(address=("localhost", 9000), authkey=b'123')