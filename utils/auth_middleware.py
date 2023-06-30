from django.contrib.sessions.models import Session

class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            stored_session_key = request.user.logged_in_user.session_key
            # if there is a stored_session_key  in our database and it is
            # different from the current session, delete the stored_session_key
            # session_key with from the Session table
            if stored_session_key and stored_session_key != request.session.session_key:
                if request.user.is_admin or request.user.is_superuser:
                    pass
                else:
                    Session.objects.get(session_key=stored_session_key).delete()

                    request.user.logged_in_user.session_key = request.session.session_key
                    request.user.logged_in_user.save()

        response = self.get_response(request)

        # This is where you add any extra code to be executed for each request/response after
        # the view is called.
        # For this tutorial, we're not adding any code so we just return the response

        return response




from django.contrib.sessions.models import Session
from authenticate.models import LoggedInUser

class OneSessionPerUserMiddleware:
    # Called only once when the web server starts
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        if request.user.is_authenticated:
            print(request.session.session_key)
            stored_session_key_, new = LoggedInUser.objects.get_or_create(
                user=request.user,

            )
            stored_session_key = stored_session_key_.session_key
            print("Session Key")

            print(stored_session_key)
            # stored_session_key = request.user.logged_in_user.session_key
            # if there is a stored_session_key  in our database and it is
            # different from the current session, delete the stored_session_key
            # session_key with from the Session table
            if stored_session_key != None and stored_session_key != request.session.session_key:
                if request.user.is_admin or request.user.is_superuser:
                    pass
                else:
                    try:
                        Session.objects.get(session_key=stored_session_key).delete()
                        print("Deleted")
                        stored_session_key_.session_key = request.session.session_key
                        print("Save")
                        print(stored_session_key_.session_key)
                        stored_session_key_.save()
                    except:
                        stored_session_key_.session_key = request.session.session_key
                        print("Save")
                        print(stored_session_key_.session_key)
                        stored_session_key_.save()
            else:
                stored_session_key_.session_key = request.session.session_key
                print("Set")

                print(stored_session_key_.session_key)
                stored_session_key_.save()

                    # request.user.logged_in_user.session_key = request.session.session_key
                    # request.user.logged_in_user.save()
        response = self.get_response(request)

        # This is where you add any extra code to be executed for each request/response after
        # the view is called.
        # For this tutorial, we're not adding any code so we just return the response

        return response