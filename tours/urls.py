from django.urls import path

from .views import (
    BaseView,
    ToursDetailView,
    CategoryDetailView,
    ContactsView,
    FaqView
)

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('tours/<str:slug>/', ToursDetailView.as_view(), name='tours_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='tours_categories'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('F.A.Q/', FaqView.as_view(), name='faq')
]
