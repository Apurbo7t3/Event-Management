from django.urls import path
from events.views import home,dashboard,create_category,create_event,create_participant,category_filter,search_filter,update_event,delete_event
urlpatterns = [
    path('home/',home,name='home'),
    path('dashboard/',dashboard,name='dashboard'),
    path('create-category/',create_category,name='create-category'),
    path('create-event/',create_event,name='create-event'),
    path('create-participant/',create_participant,name='create-participant'),
    path('category-filter/<int:id>/',category_filter,name='category-filter'),
    path('update-event/<int:id>/',update_event,name='update-event'),
    path('delete-event/<int:id>/',delete_event,name='delete-event'),
    path('search-filter/',search_filter,name='search'),
]
