
import os
import yaml
import psutil
from multiprocessing import Pool

'''*******************************************************************************
**********************************************************************************
*******************************************************************************'''
class MM_BaseList():

    def __init__(self):

        self.objects = []

    def add(self,obj):

        self.objects.append(obj)  

    def remove(self,obj):

        self.objects.remove(obj)  

    def remove_by_attribute(self,attribute,value):

        _item = self.find_by_attribute(attribute,value)

        if _item != None:

            self.remove(_item)

    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt = ""
        
        for obj in self.objects:

            _txt += str(obj)

        return _txt

    def __iter__(self):

        for obj in self.objects:

            yield obj

    def __getitem__(self,index):

        return self.objects[index]

    def __len__(self):

        return len(self.objects)

    def find_by_attribute(self,attribute,value):

        _object = None

        for _obj in self.objects:

            if getattr(_obj,attribute) == value:

                _object = _obj

        return _object

    def __add__(self,other):

        self.objects += other.objects

        return self

    def reverse(self):

        self.objects.reverse()

'''*******************************************************************************
**********************************************************************************
*******************************************************************************'''
class MM_Config():

    def __init__(self):

        self.programs = [{"name":"program1","time":1},{"name":"program2","time":1}]

    def load(self):

        _path = self.get_path()

        with open(_path) as _file:

            try:
                _data= yaml.load(_file, Loader=yaml.Loader)
            except:
                print("error: could not load configuration file %s" % (_path,))

            if "programs" in list(_data.keys()):

                self.programs = _data["programs"]
            else:
                print("error: could not load configuration file %s" % (_path,))

    def get_path(self):

        _path = os.path.join(os.path.expanduser("~"),".mm")

        if not os.path.exists(_path):

            os.mkdir(_path)

        _path = os.path.join(_path,"config.yml")

        if not os.path.exists(_path):

            with open(_path) as _file:

                yaml.dump(self.programs, _file, default_flow_style=False)

        return _path

'''*******************************************************************************
**********************************************************************************
*******************************************************************************'''
class MM_Process():

    def __init__(self,proc):

        self.proc   = proc
        self.pid    = proc.pid
        self.name   = proc.name()
        self.cpu    = 0
        self.memory = 0
        self.status = proc.status()

    def refresh(self,time=1):

        self.name   = self.proc.name()
        self.cpu    = self.proc.cpu_percent(time)
        self.memory = round(self.proc.memory_percent(),2)
        self.status = self.proc.status()

    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt = ""
        _txt += "   name [%s] "   % (self.name)
        _txt += "   pid [%s] "    % (self.pid)
        _txt += "   status [%s] " % (self.status)
        _txt += "   cpu [%s%%] "    % (self.cpu)
        _txt += "   memory [%s%%] " % (self.memory)
        _txt += '\n'

        return _txt

'''*******************************************************************************
**********************************************************************************
*******************************************************************************'''
class MM_Processes(MM_BaseList):

    def __init__(self):

        MM_BaseList.__init__(self)

    def cpu(self):

        _cpu = 0

        for _object in self.objects:

            _cpu += _object.cpu

        return round(_cpu,2)

    def memory(self):

        _memory = 0

        for _object in self.objects:

            _memory += _object.memory

        return round(_memory,2)

'''*******************************************************************************
**********************************************************************************
*******************************************************************************'''
class MM_Program():

    def __init__(self):

        self.name      = ""
        self.time      = 0
        self.cpu       = 0
        self.memory    = 0
        self.processes = MM_Processes()

    def refresh(self):

        for _process in self.processes:

            _process.refresh(self.time)

        self.cpu    = self.processes.cpu()
        self.memory = self.processes.memory()

    def __repr__(self):

        return self.__print()

    def __str__(self):

        return self.__print()

    def __print(self):

        _txt = ""
        _txt += "name [%s] "   % (self.name)
        _txt += "time [%s] "   % (self.time)
        _txt += "cpu [%s%%] "    % (self.cpu)
        _txt += "memory [%s%%] " % (self.memory)
        _txt += '\n'
        _txt += str(self.processes)
        _txt += '\n'

        return _txt

'''*******************************************************************************
**********************************************************************************
*******************************************************************************'''
class MM_Programs(MM_BaseList):

    def __init__(self):

        MM_BaseList.__init__(self)

'''*******************************************************************************
**********************************************************************************
*******************************************************************************'''
class MM_Monitor():

    def __init__(self):

        self.config   = MM_Config()
        self.config.load()

        self.programs = MM_Programs()

        for _program in self.config.programs:

            _prg = MM_Program()

            self.programs.add(_prg)

            _prg.name = _program["name"]
            _prg.time = _program["time"]

    def start(self):

        for _proc in psutil.process_iter():

            for _program in self.programs:

                if _proc.name() == _program.name:

                    _program.processes.add(MM_Process(_proc))

        for _program in self.programs:

            _program.refresh()

        print(self.programs)

    def stop(self):

        pass

'''*******************************************************************************
**********************************************************************************
*******************************************************************************'''
if __name__ == "__main__":

    _monitor = MM_Monitor()

    _monitor.start()