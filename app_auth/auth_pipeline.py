from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.urlresolvers import reverse

#from khafre.settings import REDIRECT_WITH_ACCESS_TOKEN_URL_NAME


def redirect_with_access_token(backend, strategy, *args, **kwargs):
    """
     Add access_token, provider, expires to the redirection URL
     if request argument is ?next=/api/profile/
     Final redirection is done in 'social.actions.do_complete'
     Token is taken from
        1) for social network OAUTH2 Provider -> social.extra_data :  {u'access_token': u'c3aa642377182bc0b537c95da282c1ccf05b6915', u'login': u'vfdev-5', u'expires': None, u'id': 2459423}
        or
        2) for local OAUTH2 Provider -> response : {'username': u'userone', 'first_name': u'John', 'last_name': u'Smith', u'access_token': u'cVkeByo5MSr09duwG8fUvKdA7D7BUT', u'expires_in': 36000, u'token_type': u'Bearer', 'groups': <django.db.models.fields.related.ManyRelatedManager object at 0x7f179853131

    """
    print "redirect_with_access_token"


    # check if next == REDIRECT_WITH_ACCESS_TOKEN_URL
    redirect_uri = strategy.session_get(REDIRECT_FIELD_NAME)
    # print "redirect_uri:", redirect_uri
    # print "reverse(REDIRECT_WITH_ACCESS_TOKEN_URL_NAME):", reverse(REDIRECT_WITH_ACCESS_TOKEN_URL_NAME)
    if redirect_uri and redirect_uri == reverse(REDIRECT_WITH_ACCESS_TOKEN_URL_NAME):
        access_token = None
        expires = None
        social = kwargs.get('social', None)
        response = kwargs.get('response', None)
        print "Social: ", social
        print "Response: ", response
        if social :
            access_token = social.extra_data['access_token']
            expires = social.extra_data['expires']
        elif response:
            access_token = response['access_token']
            expires = response['expires_in']
        else:
            return

        redirect_uri+="?access_token="+access_token
        redirect_uri+="&provider="+backend.name
        redirect_uri+="&expires="+str(expires)
        strategy.session_set(REDIRECT_FIELD_NAME, redirect_uri)

