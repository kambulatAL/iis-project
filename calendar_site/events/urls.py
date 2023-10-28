from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name='home_page'),
    path('events/', views.create_event, name='new_event_page'),
    # Возможно в будущем пригодится Камбулат
    #path('events/<int:event_id>', views.event_page, name='event_page'),

    path('category/', views.create_category, name='new_category_page'),
]


# user authentication paths
urlpatterns += [
    path('login/', views.login_view, name='login_page'),
    path('register/', views.register_view, name='register_page'),
    path('logged', views.logout_view, name='logout_page')
]


# admin paths
urlpatterns += [
    path('admin_page/', views.admin_view, name='admin_page'),
    path('admin_page/users/', views.list_users, name='list_users_page'),
    path('admin_page/users/delete_user/<str:username>/', views.delete_user, name='delete_user_page'),
    path('admin_page/places/', views.list_places, name='list_places_page'),
]