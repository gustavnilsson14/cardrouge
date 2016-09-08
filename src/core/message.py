import json,inspect

class JoinableObject():

    method_index = {}

    def __init__(self,queues):
        self.__class__.method_index = self.__class__.methods_to_ints()
        self.queues = queues

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
        while not self.queues.get('input').empty():
            message = self.queues.get('input').get()
            if message.to != None:
                pass
            self.run_method_by_index(message.method,message.data)

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
