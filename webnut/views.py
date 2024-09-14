from pyramid.exceptions import NotFound
from pyramid.renderers import get_renderer, render
from pyramid.view import view_config

from .webnut import WebNUT
from . import config

NAVBAR_LIST_LIMIT = 4

class NUTViews(object):
    def __init__(self, request):
        self.request = request
        renderer = get_renderer("templates/layout.pt")
        self.layout = renderer.implementation().macros['layout']
        self.webnut = WebNUT(config.server, config.port,
                config.username, config.password)

    def _get_layout_context(self):
        return {
            'ups_navbar': self.webnut.get_ups_list(limit=NAVBAR_LIST_LIMIT)
        }

    @view_config(route_name='home', renderer='templates/index.pt')
    def home(self):
        context = dict(
                    title='UPS Devices',
                    ups_list=self.webnut.get_ups_list()
                )
        context.update(self._get_layout_context())
        return context

    @view_config(route_name='ups_view', renderer='templates/ups_view.pt')
    def ups_view(self):
        ups = self.request.matchdict['ups']
        try:
            ups_name = self.webnut.get_ups_name(ups)
            ups_vars = self.webnut.get_ups_vars(ups)
            vars = dict(
                ups_vars=ups_vars[0],
                ups_status=ups_vars[1]
            )
            charts = render('templates/components/ups_charts.pt', vars, request=self.request)
            table = render('templates/components/ups_datatable.pt', vars, request=self.request)
            context = dict(
                title=ups_name,
                ups_vars=ups_vars[0],
                ups_status=ups_vars[1],
                charts=charts,
                table=table
            )
            context.update(self._get_layout_context())
            return context
        except KeyError:
            raise NotFound

def notfound(request):
    request.response.status = 404
    return dict(title='No Such UPS')
