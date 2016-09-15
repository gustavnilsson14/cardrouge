from log import Log
import json,inspect,sys
from multiprocessing import Process, Queue

class JoinableObject(Log):

    JOIN_LIMIT = 100

    method_index = {}

    def __init__(self,queues):
        self.__class__.method_index = self.__class__.methods_to_ints()
        self.queues = queues
        self.child_processes = []

    @classmethod
    def methods_to_ints(cls,foreign_reference = 0):
        method_index = {}
        for index, item in enumerate(dir(cls)):
            if foreign_reference:
                method_index[str(item)] = index
                continue
            method_index[index] = str(item)
        return method_index

    def run_method_by_index(self,index,data):
        method = self.__class__.method_index.get(index)
        getattr(self,method)(data)

    def join(self):
        joined_data = 0
        while not self.queues.get('input').empty() and joined_data < JoinableObject.JOIN_LIMIT:
            joined_data += 1
            message = self.queues.get('input').get()
            if message.to != None:
                pass
            if message.method == 'terminate':
                self.terminate()
                return
            self.run_method_by_index(message.method,message.data)
        if joined_data == JoinableObject.JOIN_LIMIT:
            print("FUUUUU")
        return joined_data

    def run(self,method,data):
        method_class_name = method.__qualname__.split('.')[0]
        method_name = method.__name__
        if not self.__class__.method_index.get(method_class_name):
            method_class = self.get_class_of_method(method)
            self.__class__.method_index[method_class_name] = method_class.methods_to_ints(1)
        method = self.__class__.method_index[method_class_name].get(method_name)
        message = Message(method,data)
        self.queues.get(method_class_name).put(message)

    def get_class_of_method(self,meth):
        if inspect.ismethod(meth):
            for cls in inspect.getmro(meth.__self__.__class__):
                if cls.__dict__.get(meth.__name__) is meth:
                    return cls
            meth = meth.__func__ # fallback to __qualname__ parsing
        if inspect.isfunction(meth):
            cls = getattr(inspect.getmodule(meth),meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0])
            if isinstance(cls, type):
                return cls
        return None

    def start_child_process(self,target):
        queues = {
            self.__class__.__name__: self.queues.get('input'),
            'input': self.queues.get(target.__name__)
        }
        new_process = Process(target=target,args=(queues,))
        new_process.start()
        self.child_processes += [new_process]

    def terminate(self):
        for name, queue in self.queues.items():
            if name == 'input':
                continue
            self.log('terminating %s'%(name,))
            queue.put(Message('terminate',{}))
        self.log('terminating myself')
        exit(0)

class Message:

    def __init__(self,method,data,to=None):
        self.method = method
        self.data = data
        self.to = to

class MessageError(Exception):
    def __init__(self, message, errors = []):

        # Call the base class constructor with the parameters it needs
        super(ValidationError, self).__init__(message)

        # Now for your custom code...
        self.errors = errors

class ReducableObject(Log):
    '''
    Extension for all classes which should be sent through a tcp socket.
    Handles reducing to dict objects and instantiating the extending classes on the other side
    return: None
    input;
    side effects;
    '''

    @staticmethod
    def get_cls(data):
        _module = data.get('_module')
        _cls = data.get('_cls')
        if sys.modules.get(_module):
            if sys.modules.get(_module).get(_cls):
                return sys.modules.get(_module).get(_cls)
            ReducableObject.log('no such class: %s in module: %s'%(_cls,_module,))
        ReducableObject.log('no such module: %s'%(_module,))
        return None

    @classmethod
    def init(cls,data):
        new_instance = cls()
        for key,val in data.items():
            if key == 'cls':
                continue
            setattr(new_instance,key,val)
        return new_instance

    def as_dict(self):
        data = self.__dict__
        data['_cls'] = self.__class__.__name__
        data['_module'] = self.__module__
        return data

class Test(ReducableObject):
    def __init__(self):
        self.test = 'test'
