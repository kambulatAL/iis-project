from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='home_page'),
    path('events/', views.create_event, name='new_event_page'),
    path('events/join_user_event/<int:event_id>/<str:username>/', views.join_user_event, name='event_join_user_page'),
    path('events/<int:event_id>/', views.show_event_page, name='event_page'),
    path('events/<int:event_id>/<str:username>/del_comm/', views.delete_comment, name='del_page'),
    path('events/category/<int:cat_id>', views.filter_by_category, name='category_ev_filter'),
    path('events/payment/<int:event_id>/<str:username>/', views.make_payment, name='payment_page'),
    path('events/<int:event_id>/list_of_enrolled_people/', views.list_enrolled_users, name="enrolled_people"),
    path('events/<int:event_id>/<str:username>/leave_comment/', views.leave_comment, name="leave_comment"),

    path('category/', views.create_category, name='new_category_page'),

    # My calendar page
    path('my_calendar/', views.my_calendar, name='my_calendar_page'),

    # New place page
    path('places/', views.create_place, name='new_place_page'),
]

# user authentication paths
urlpatterns += [
    path('login/', views.login_view, name='login_page'),
    path('register/', views.register_view, name='register_page'),
    path('settings/', views.settings_view, name='settings_page'),
    path('logged', views.logout_view, name='logout_page')
]

# admin paths
urlpatterns += [
    path('admin_page/', views.admin_view, name='admin_page'),
    path('admin_page/users/', views.list_users, name='list_users_page'),
    path('admin_page/users/delete_user/<str:username>/', views.delete_user, name='delete_user_page'),
    path('admin_page/users/add_moder_rights/<str:username>/', views.add_moder_rights, name='add_moder_rights'),
    path('admin_page/users/remove_moder_rights/<str:username>/', views.remove_moder_rights, name='remove_moder_rights'),
    path('admin_page/places/', views.list_places, name='list_places_page'),
    path('admin_page/events/', views.list_events, name='list_events_page'),
    path('admin_page/events/approve_event/<int:event_id>/', views.approve_event, name='approve_event_page'),
    path('admin_page/events/reject_event/<int:event_id>/', views.reject_event, name='reject_event_page'),
    path('admin_page/categories/', views.list_categories, name='list_categories_page'),
    path('admin_page/categories/approve_category/<int:category_id>/', views.approve_category,
         name='approve_category_page'),
    path('admin_page/categories/reject_category/<int:category_id>/', views.reject_category,
         name='reject_category_page'),

    path('admin_page/places/approve_place/<int:place_id>/', views.approve_place, name='approve_place_page'),
    path('admin_page/places/reject_place/<int:place_id>/', views.reject_place, name='reject_place_page'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
