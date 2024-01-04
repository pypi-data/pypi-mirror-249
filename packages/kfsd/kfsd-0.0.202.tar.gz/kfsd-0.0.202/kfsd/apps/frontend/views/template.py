from django.views.generic import TemplateView as DjangoTemplateView
from kfsd.apps.core.utils.dict import DictUtils


class BaseTemplate(DjangoTemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        configContext = DictUtils.get_by_path(self.request.config, "services.context")
        feContext = configContext if configContext else {}
        context = DictUtils.merge(dict1=context, dict2=feContext)
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context["user"] = self.request.token_user
        return self.render_to_response(context)
