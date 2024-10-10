from pyramid.events import ApplicationCreated, BeforeRender, NewRequest, subscriber
from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound
from .webnutclient import WebNUTClient
from .webnut import WebNUT
from . import config

NAVBAR_LIST_LIMIT = 4

@subscriber(ApplicationCreated)
def app_created_subscriber(event):
    """
    When the Pyramid application is created, start the WebNUTClient listener.
    """
    request = event.app.registry
    nut_client = WebNUTClient(host=config.server, port=config.port)
    nut_client.start_event_listener()
    request.nut_client = nut_client
    print("Started UPS event listener.")



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('ups_view', '/{ups}')
    config.add_view('webnut.views.notfound',
            renderer='webnut:templates/404.pt',
            context='pyramid.exceptions.NotFound')
    config.scan()
    return config.make_wsgi_app()

@subscriber(NewRequest)
def request_event_listener(event):
    """
    Attach NUTClient to every request for easy access.
    """
    event.request.nut_client = event.request.registry.nut_client


@subscriber(BeforeRender)
def add_global_context(event):
    webnut = WebNUT(config.server, int(config.port), config.username, config.password)
    event['ups_navbar'] = webnut.get_ups_list(limit=NAVBAR_LIST_LIMIT)
