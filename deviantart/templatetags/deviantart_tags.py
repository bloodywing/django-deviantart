from deviantart.oauth import Deviantart
from django import template
from django.http.request import QueryDict

register = template.Library()

@register.simple_tag()
def dA(endpoint, auth_user=None, **params):
    deviantart = Deviantart(auth_user=auth_user)
    qd = QueryDict(mutable=True)
    qd.update(params)
    return deviantart.get(endpoint + '?' + qd.urlencode())
