def func():
    print('hello')

def func_with_arg(name):
    print('hello, {}'.format(name))

class CalebIsGreat():
    def __init__(self, name):
        self.hello = name

    def say_hello(self):

        print('hello {}'.format(self.name))

    @classmethod
    def setup(cls):
        cls.second_name = 'kandoro'

    def greet_formally(self, name):
        if self.second_name:
            print('hello %s, %s' % (name, self.second_name))

    @staticmethod
    def hello_nobody():
        print('hello nobody')

    def run(self):
        CalebIsGreat.setup()
        self.say_hello(caleb)
        self.greet_formally(caleb)