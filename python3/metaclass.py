

class Metaclass(type):
    print('metaclass')

    def __new__(cls, name, bases, attrs):
        print('This is metaclass:==> ', name, bases, attrs)
        attrs['tag'] = name
        cls.something = "Hello World!"
        return type.__new__(cls, name, bases, attrs)

    # def __new__(cls, *args, **kwargs):
    #     print('This is metaclass:==> ', args, kwargs)
    #     cls.something = "Hello World!"
    #     return type.__new__(cls, *args, **kwargs)

class model(dict, metaclass=Metaclass):

    def __init__(self, **kwargs):
        print('this is model...', kwargs)
        super(model, self).__init__(**kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, key):
        try:
            return self[key]
        except:
            return r"'{}' object has no attribute '{}'" .format(model.__name__,key)


class Info(model):
    print('This is info ...')
    s = 'hello'
    n = "world"
    def __init__(self, **kwargs):
        print('This is info __init__....')

    def __new__(cls, *args, **kwargs):
        print("this is info __new__....",args, kwargs, cls.something)
        return model.__new__(cls, *args, **kwargs)

# class User(model):
#     name = 'zhangsan'
#     age = 20

i = Info(a='jj')
# u = User()
print(i.s, i.something, i.tag, Info.something, Info.tag)
print(i.__dict__,  '\n', Info.__dict__, '\n', model.__dict__)











class People:
    a = 'a'

class user(People):
    s = 's'

p = People()
People.b = 'b'
p.c = 'c'
print(p.a, p.b, p.c)