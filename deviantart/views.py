from django.http.response import HttpResponseServerError
from django.shortcuts import redirect, render, reverse

from .oauth import Deviantart


def callback(request):
    try:
        deviantart = Deviantart(request.session['redirect_uri'], auth_user=request.user)
    except KeyError:
        return auth(request)
    code = request.GET['code']
    deviantart.fetch_token(code)
    return redirect('/')


def auth(request):
    request.session['redirect_uri'] = request.build_absolute_uri(
        reverse('deviantart-cb')
    )
    deviantart = Deviantart(request.session['redirect_uri'], auth_user=request.user)
    return redirect(deviantart.auth_url)


def endpoint(request, dapath):
    params = request.GET
    deviantart = Deviantart(auth_user=request.user)
    json = deviantart.get(dapath + ('?' + params.urlencode() if params else ''))
    status_code = json.get('error_code', 200)

    if json.get('error_code', 200) >= 400:
        return HttpResponseServerError(status=status_code)

    return render(request,'deviantart/endpoint.html', json)
