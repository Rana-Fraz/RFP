#Session model stores the session data
from django.contrib.sessions.models import Session
from .signals import *
class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # cur_session_key = request.user.LoggedInUser.session_key
        # if cur_session_key and cur_session_key != request.session.session_key:
        #     Session.objects.get(session_key=cur_session_key).delete()
        # # the following can be optimized(do not save each time if value not changed)
        # request.user.LoggedInUser.session_key = request.session.session_key
        # request.user.LoggedInUser.save()








        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            print("In function")
            #stored=LoggedInUser.objects.get_or_create(session_key=request.session.session_key,user=request.user)
            stored=LoggedInUser.objects.get(user=request.user)
            stored.session_key = request.session.session_key

            # if there is a stored_session_key  in our database and it is
            # different from the current session, delete the stored_session_key
            # session_key with from the Session table
            if stored.session_key != request.session.session_key:
                Session.objects.get(session_key=stored.session_key).delete()

            stored.session_key = request.session.session_key
            stored.save()

        response = self.get_response(request)

        # This is where you add any extra code to be executed for each request/response after
        # the view is called.
        # For this tutorial, we're not adding any code so we just return the response

        return response