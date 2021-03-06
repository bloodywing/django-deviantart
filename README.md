# django-deviantart
Oauth2 Django App for Deviantart

## Installation

    pip install django-deviantart

add deviantart to your settings.

    INSTALLED_APPS = [
    ...
    'deviantart'
    ]
    
Go to [the deviantart developer program](http://www.deviantart.com/developers/register) and register
an application. Don't worry unless you submit it to the gallery no one will see it.

Run migrations
    
    ./manage.py migrate

Go back to your settings and add your `client_id`, `client_secret` and some scopes.

    DEVIANTART_CLIENT_ID = '1234'  # this should be just a number
    DEVIANTART_CLIENT_SECRET = 'sha1 hash'  # Press show on the deviantart site
    DEVIANTART_SCOPE = ['browse', 'user']  # You can find more informations about the scopes on the deviantart site

Add the oauth2 urls to your **urls.py**

    from deviantart import urls as deviantart_urls
    
    urlpatterns += [
        url(r'^deviantart/', include(deviantart_urls)),
    ]
    
Now open your browser at `deviantart/auth` [Click here if you run the default testserver](http://127.0.0.1:8000/deviantart/auth)
If you've done everything right your should be redirected to the deviantart site where you need to press **authorize**

## Attention

If you change your scope you need to reauth your app be open the auth link from above again

## Future plans for django-deviantart

* make it easier to use
* Useable django authbackend for this
* reuseable templates
* more examples
