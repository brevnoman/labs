from django.views.generic.detail import SingleObjectMixin
from mainapp.models import Category


class CategoryContextMixin(SingleObjectMixin):

    def get_context_data(self, **kwargs):
        category_qs = Category.objects.all()
        context = super().get_context_data(**kwargs)
        context['categories'] = category_qs
        return context
