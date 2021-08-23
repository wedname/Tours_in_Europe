from django.shortcuts import render
from django.views.generic import DetailView, View, ListView

from .models import ToursInEurope, TourCategories


class BaseView(ListView):
    model = ToursInEurope
    context_object_name = 'tours'
    template_name = 'tours/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = TourCategories.objects.raw("""select tours_tourcategories.id 
                from tours_toursineurope, tours_tourcategories
                where tours_tourcategories.id = tours_toursineurope.type_id
                group by tours_tourcategories.name""")
        return context


class ToursDetailView(DetailView):
    model = ToursInEurope
    context_object_name = 'tour'
    template_name = 'tours/tours_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['tour'].name
        context['categories'] = self.get_object().type.__class__.objects.raw("""select tours_tourcategories.id 
        from tours_toursineurope, tours_tourcategories
        where tours_tourcategories.id = tours_toursineurope.type_id
        group by tours_tourcategories.name""")
        return context


class CategoryDetailView(DetailView):
    model = TourCategories
    context_object_name = 'category'
    template_name = 'tours/category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Тип - ' + str(context['category'].name)
        context['categories'] = TourCategories.objects.raw("""select tours_tourcategories.id
            from tours_toursineurope, tours_tourcategories
            where tours_tourcategories.id = tours_toursineurope.type_id
            group by tours_tourcategories.name""")
        context['tours'] = ToursInEurope.objects.filter(type__name=context['category'].name)
        return context


class ContactsView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'tours/contacts.html')


class FaqView(View):

    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'tours/faq.html')
