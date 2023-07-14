menu = ['home', 'schedule', 'diverted', 'cancelled',]

class DataMixin:
    paginate_by = 3
    def get_user_context(self, **kwargs): #Form the necessary context by default
        context = kwargs #Create a dictionary from passed parametrs
        context['menu'] = menu
        return context
