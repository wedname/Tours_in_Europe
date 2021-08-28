from django.shortcuts import render
from django.views.generic import DetailView, View, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect

from .models import ToursInEurope, TourCategories
from users.models import Customer
from .filters import ToursFilter


class FilterToursListView(ListView):

    filter_class = None

    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        req = self.request.GET
        self.filtered = self.filter_class(req, qs)
        return self.filtered.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filtered
        return context


class BaseView(FilterToursListView):
    model = ToursInEurope
    filter_class = ToursFilter
    context_object_name = 'tours'
    template_name = 'tours/index.html'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = TourCategories.objects.filter(toursineurope__type__name__isnull=False).distinct()
        return context


class ToursDetailView(DetailView):
    model = ToursInEurope
    context_object_name = 'tour'
    template_name = 'tours/tours_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['tour'].name
        context['categories'] = self.get_object().type.__class__.objects.filter(
            toursineurope__type__name__isnull=False).distinct()
        context['user'] = Customer.objects.filter(user=self.request.user)
        context['is_followed_tour'] = Customer.objects.filter(
            user=self.request.user, tours_registration__slug=self.kwargs['slug']).first()
        return context


class CategoryDetailView(DetailView):
    model = TourCategories
    context_object_name = 'category'
    template_name = 'tours/category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Тип - ' + str(context['category'].name)
        context['categories'] = TourCategories.objects.filter(toursineurope__type__name__isnull=False).distinct()
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
        'country',
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
        'country',
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
        tour_slug = kwargs.get('slug')
        tour = ToursInEurope.objects.get(slug=tour_slug)
        customer = Customer.objects.get(user=request.user)
        customer.tours_registration.add(tour)
        customer.save()
        return HttpResponseRedirect('/')

    def test_func(self):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect('/login/')
        user = Customer.objects.filter(user=self.request.user).first()
        return self.request.user == user.user


class DeleteTourView(UserPassesTestMixin, LoginRequiredMixin, View):

    @staticmethod
    def get(request, *args, **kwargs):
        tour_slug = kwargs.get('slug')
        tour = ToursInEurope.objects.get(slug=tour_slug)
        customer = Customer.objects.get(user=request.user)
        customer.tours_registration.remove(tour)
        customer.save()
        return HttpResponseRedirect('/')

    def test_func(self):
        if self.request.user.is_anonymous:
            return HttpResponseRedirect('/login/')
        user = Customer.objects.filter(user=self.request.user).first()
        return self.request.user == user.user


def error404(request, exception):
    if "tried" in str(exception):
        context = {"exception": "page not found"}
    else:
        context = {"exception": exception}
    return render(request, "tours/404.html", context)


def error403(request, exception):
    context = {"exception": exception}
    return render(request, "tours/404.html", context)


def error500(request,):
    context = {"exception": 'Сервер не отвечает'}
    return render(request, "tours/404.html", context)
