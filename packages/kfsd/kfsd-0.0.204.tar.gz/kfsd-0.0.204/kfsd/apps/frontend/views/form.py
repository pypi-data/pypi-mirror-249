from django.views.generic import FormView as DjangoFormView
from kfsd.apps.frontend.views.template import BaseTemplate


class BaseForm(BaseTemplate, DjangoFormView):
    pass
