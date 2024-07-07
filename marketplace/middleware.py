from django.shortcuts import redirect
from django.urls import reverse_lazy
import collection
import api.urls
import collection.urls

#FIXATO dopo la consegna
class SelectionModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.session.get('selection', None) and not self.check_excluded_path(request): 
            redirect_url = reverse_lazy('collection:game_list')
            return redirect(f'{redirect_url}?selection_redirect=1')

        return self.get_response(request)
    
    def check_excluded_path(self, request):
        app = request.path.split('/')[1]

        excluded_paths = [
            reverse_lazy('marketplace:end_selection'),
            reverse_lazy('marketplace:start_in_exchange_selection')
        ]
        if request.path in excluded_paths:
            return True
        if app == collection.urls.app_name or app == api.urls.app_name:
            return True
        return False