from .models import Listing
from django.shortcuts import get_object_or_404

def set_selection_mode(request, status, selection_dest = None, listing_id = None):
    if not request.user.is_authenticated:
        return False
    
    if not all(key in request.session for key in ['selection_dest', 'listing_id', 'selection']):
        clear_session(request.session)
    
    if not status:
        clear_session(request.session)
        return True

    if not selection_dest or not listing_id:
        clear_session(request.session)
        return False

    listing = get_object_or_404(Listing, user=request.user, id=listing_id)
    request.session['selection'] = True
    request.session['selection_dest'] = selection_dest
    request.session['listing_id'] = listing_id
    
    return True
                
def clear_session(session):
    session['selection'] = False
    session['selection_dest'] = None
    session['listing_id'] = None