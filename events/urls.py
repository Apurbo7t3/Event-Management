from django.urls import path
from events.views import home,dashboard,event_rsvp,account_activate,group_page,delete_group,show_participant,update_participant,delete_participant,create_category,create_event,create_participant,category_filter,search_filter,update_event,delete_event,create_group
urlpatterns = [
    path('home/',home,name='home'),
    path('dashboard/',dashboard,name='dashboard'),
    path('create-category/',create_category,name='create-category'),
    path('create-event/',create_event,name='create-event'),
    path('create-participant/',create_participant,name='create-participant'),
    path('create-group/',create_group,name='create-group'),
    path('category-filter/<int:id>/',category_filter,name='category-filter'),
    path('update-event/<int:id>/',update_event,name='update-event'),
    path('delete-event/<int:id>/',delete_event,name='delete-event'),
    path('search-filter/',search_filter,name='search'),
    path('rsvp/<int:user_id>/<int:event_id>/',event_rsvp,name='rsvp'),
    path('delete-participant/<int:user_id>/',delete_participant,name='delete-participant'),
    path('update-participant/<int:user_id>/',update_participant,name='update-participant'),
    path('participant-page/',show_participant,name='participant-page'),
    path('group-page/',group_page,name='group-page'),
    path('delete-group/<int:grp_id>/',delete_group,name='delete-group'),
    path('activate/<int:user_id>/<str:token>/',account_activate,name='account-activate')
]
