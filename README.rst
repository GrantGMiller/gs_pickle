gs_pickle
=========
A helper to convert objects to/from strings for persistent storage.

Usage
=====
You will need to create 2 helper functions and register them with the pickler.
One function, the "dumper" should convert the object to a string.
The other function, the "loader" should convert the string back into the object.

Example
=======

::

     pickler = Pickler()


    def DumperDict(d):
        # this is pretty much useless because you could just use json.dumps,
        #   but it gives you an idea.
        return json.dumps(d)


    pickler.RegisterDumper(dict, DumperDict)


    def LoaderDict(j):
        return json.loads(j)


    pickler.RegisterLoader(dict, LoaderDict)

    d = {'one': 1, 'two': 2}

    s = pickler.Dumps(d)
    print('s=', s)
    >>> s= {"type(obj).__module__": "builtins", "type(obj).__name__": "dict", "dumper_string": "{\"one\": 1, \"two\": 2}"}

    d2 = pickler.Loads(s)
    print('d2=', d2)
    >>> d2= {'one': 1, 'two': 2}

    ####################
    class CustomClass:
        def __init__(self, name):
            self.name = name

        def __str__(self):
            return '<CustomClass: name={}>'.format(self.name)


    def DumperCustomClass(obj):
        return json.dumps({'name': obj.name})


    pickler.RegisterDumper(CustomClass, DumperCustomClass)


    def LoaderCustomClass(strng):
        d = json.loads(strng)
        return CustomClass(name=d['name'])


    pickler.RegisterLoader(CustomClass, LoaderCustomClass)

    obj = CustomClass('me')
    s = pickler.Dumps(obj)
    print('s=', s)
    >>> s= {"type(obj).__module__": "__main__", "type(obj).__name__": "CustomClass", "dumper_string": "{\"name\": \"me\"}"}

    obj2 = pickler.Loads(s)
    print('obj2=', obj2)
    >>> obj2= <CustomClass: name=me>