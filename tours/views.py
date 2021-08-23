from django.shortcuts import render
from django.views.generic import DetailView, View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import ToursInEurope, TourCategories
from users.models import Customer


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


class TourCreateView(LoginRequiredMixin, CreateView):
    model = ToursInEurope
    fields = [
        'slug',
        'image',
        'name',
        'type',
        'description',
        'price'
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание тура'
        context['button'] = 'Создать'
        return context


class TourUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = ToursInEurope
    fields = [
        'slug',
        'image',
        'name',
        'type',
        'description',
        'price'
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        tour = self.get_object()
        return self.request.user == tour.author

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование тура'
        context['button'] = 'Обновить'
        return context


class TourDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = ToursInEurope
    success_url = '/profile/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class AddTourView(UserPassesTestMixin, LoginRequiredMixin, View):

    @staticmethod
    def get(request, *args, **kwargs):
        pass

    def test_func(self):
        user = Customer.objects.filter(user=self.request.user).first()
        return self.request.user == user.user
