from kfsd.apps.frontend.views.template import BaseTemplate


class Custom500View(BaseTemplate):
    template_name = "v1/errors/500.html"
