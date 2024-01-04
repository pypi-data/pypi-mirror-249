from kfsd.apps.frontend.views.template import BaseTemplate


class Custom403View(BaseTemplate):
    template_name = "v1/errors/403.html"
