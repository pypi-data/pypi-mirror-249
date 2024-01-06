import supabase

__version__ = "0.1.2"

def Client():
    # TODO dont hard code this
    supabase_url: str = 'https://api.humata.ai'
    supabase_anon_key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJlbnpmb2RxdWF0amNheHFoYm1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzI0Mzg4MDYsImV4cCI6MTk4ODAxNDgwNn0.5YmrDS0ie09qbFdRBZpX9ygXQSi82F5g25tRk57OKT4'
    return supabase.create_client(url, supabase_anon_key)

class Number(object):

    def __init__(self, n):
        self.value = n

    def val(self):
        return self.value

    def add(self, n2):
        self.value += n2.val()

    def __add__(self, n2):
        return self.__class__(self.value + n2.val())

    def __str__(self):
        return str(self.val())

    @classmethod
    def addall(cls, number_obj_iter):
        cls(sum(n.val() for n in number_obj_iter))
