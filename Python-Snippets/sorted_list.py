# ref: https://stackoverflow.com/questions/1109804/does-python-have-a-sorted-list
import bisect

class sortedlist(list):
    '''just a list but with an insort (insert into sorted position)'''
    def insert(self, x):
        bisect.insort(self, x)