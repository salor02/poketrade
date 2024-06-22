from django.shortcuts import redirect
from django.urls import reverse_lazy
import collection
import collection.urls

class SelectionModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not self.check_excluded_path(request) and request.session['selection']:
            return redirect(reverse_lazy('collection:game_list'))

        return self.get_response(request)
    
    def check_excluded_path(self, request):
        app = request.path.split('/')[1]
        print(request.path)
        print(reverse_lazy('marketplace:end_selection'))
        if request.path == reverse_lazy('marketplace:end_selection') and request.path == reverse_lazy('marketplace:start_in_exchange_selection'):
            return True
        if app == collection.urls.app_name:
            return True
        return False