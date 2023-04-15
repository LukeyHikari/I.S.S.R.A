import tempfile
from datetime import datetime
import time
import os

class tempmanager:
    def __init__(self):
        self.noofstudents = 5
        self.samplegrades = []
        self.path = 'App/temp/'
        self.gradesread = []
        self.recordinggrades = []
    
    def create(self): #Function to be called everytime a grading instance is started
        if os.listdir(self.path) == []:
            now = datetime.now()
            dateandtime = now.strftime("%d%m%Y%H%M")
            temp = tempfile.NamedTemporaryFile(prefix="grades_", suffix=f'_{dateandtime}',
                                               delete=False, dir = 'App/temp/', mode = 'w+t')
        else:
            pass

    def tempw(self, _noofstudents): #Function to be called after a gradeset has been defined
        tempfilename = os.listdir(self.path)
        temppath = tempfilename[0]
        f = open(f'{self.path}{temppath}', 'r')
        exist = f.readline()
        self.noofstudents = _noofstudents
        if exist != '':
            #Already has grades so don't write
            f.close()
        else:
            f.close()
            f = open(f'{self.path}{temppath}', 'a')
            for x in range(self.noofstudents):
                f.write(f'{self.gradesread[x]}\n')
            f.close()
    
    def tempr(self): #Function to be called when finally recording grades (returns an array of grades)
        tempfilename = os.listdir(self.path)
        temppath = tempfilename[0]
        f = open(f'{self.path}{temppath}', 'r')
        exist = f.readline()
        if exist != '':
            f.close()
            f = open(f'{self.path}{temppath}', 'r')
            self.gradesread = f.readlines()
            for x in self.gradesread:
                self.recordinggrades.append(x.replace("\n", ""))
            #print(f'{self.recordinggrades[0]}{self.recordinggrades[1]}')
            f.close() 
        else:
            print('No grades found')
            f.close()
        return self.recordinggrades