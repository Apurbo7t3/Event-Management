from django.contrib import admin
from django.urls import include, path
from participant.views import participant_home,participant_category_filter,participant_search_filter,participant_dashboard

urlpatterns = [
    path('participant-home/',participant_home,name='participant-home'),
    path('participant-category-filter/<int:id>/',participant_category_filter,name='participant-category-filter'),
    path('partcipant-search-filter/',participant_search_filter,name='partcipant-search-filter'),
    path('participant-dashboard/<int:user_id>/',participant_dashboard,name='participant-dashboard')
]
