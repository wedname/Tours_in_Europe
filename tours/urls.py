from django.urls import path

from .views import (
    BaseView,
    ToursDetailView,
    CategoryDetailView,
    ContactsView,
    FaqView,
    TourCreateView,
    TourUpdateView,
    TourDeleteView,
    AddTourView,
    DeleteTourView,
)

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('tours/<str:slug>/', ToursDetailView.as_view(), name='tours_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='tours_categories'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('F.A.Q/', FaqView.as_view(), name='faq'),
    path('tour/new/', TourCreateView.as_view(), name="tour_create"),
    path('tour/<str:slug>/update/', TourUpdateView.as_view(), name="tour-update"),
    path('tour/<str:slug>/delete/', TourDeleteView.as_view(), name="tour-delete"),
    path('add-tour/<str:slug>/', AddTourView.as_view(), name='add_tour'),
    path('delete-tour/<str:slug>/', DeleteTourView.as_view(), name='delete_tour'),
]


