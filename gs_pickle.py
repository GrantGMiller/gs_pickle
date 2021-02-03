import json
from collections import defaultdict

TYPE_OBJ_NAME = 'type(obj).__name__'
TYPE_OBJ_MODULE = 'type(obj).__module__'
DUMPER_STRING = 'dumper_string'


class Pickler:
    def __init__(self, debug=True):
        self.debug = debug

        ##############
        self.dumpers = defaultdict(dict)  # {
        # str(__module__):{
        # cls: dumperFunction
        #
        # }

        self.loaders = defaultdict(dict)  # {
        # str(__module__):{
        # type(cls).__name__: dumperFunction
        #
        # }
        #

    def RegisterDumper(self, cls, dumper):
        '''

        :param cls:
        :param dumper: function should take one param 'obj' and return a string.
        This string will be used by the loader to reconstruct the obj
        :return:
        '''
        self.dumpers[cls.__module__][cls] = dumper
        self.print('Pickler.dumpers=', self.dumpers)

    def RegisterLoader(self, cls, loader):
        '''

        :param cls:
        :param loader: function that accepts a string and returns the obj
        :return:
        '''
        self.loaders[cls.__module__][cls.__name__] = loader
        self.print('Pickler.loaders=', self.loaders)

    def print(self, *a, **k):
        if self.debug:
            print(*a, **k)

    def Dumps(self, obj):
        self.print('Pickler.Dumps(obj=', obj)
        if type(obj) not in self.dumpers[type(obj).__module__]:
            raise TypeError('Unrecognized type "{}". You must call "Pickler.RegisterDumper(cls, func)" first.'.format(
                type(obj)
            ))

        d = {
            TYPE_OBJ_MODULE: type(obj).__module__,
            TYPE_OBJ_NAME: type(obj).__name__,
            DUMPER_STRING: self.dumpers[type(obj).__module__][type(obj)](obj)
        }

        return json.dumps(d)

    def Loads(self, strng):
        self.print('Pickler.Loads(obj=', strng)
        d = json.loads(strng)
        if d[TYPE_OBJ_NAME] not in self.loaders[d[TYPE_OBJ_MODULE]]:
            raise TypeError('Unrecognized type "{}". You must call "Pickler.RegisterDumper(cls, func)" first.'.format(
                d[TYPE_OBJ_NAME]
            ))

        loader = self.loaders[d[TYPE_OBJ_MODULE]][d[TYPE_OBJ_NAME]]
        return loader(d[DUMPER_STRING])


class Rick(Pickler):
    # a joke in honor of AR
    pass


if __name__ == '__main__':
    pickler = Pickler()


    def DumperDict(d):
        return json.dumps(d)


    pickler.RegisterDumper(dict, DumperDict)


    def LoaderDict(j):
        return json.loads(j)


    pickler.RegisterLoader(dict, LoaderDict)

    d = {'one': 1, 'two': 2}

    s = pickler.Dumps(d)
    print('s=', s)

    d2 = pickler.Loads(s)
    print('d2=', d2)


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

    obj2 = pickler.Loads(s)
    print('obj2=', obj2)
