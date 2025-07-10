from django.urls import path # type: ignore
from . import views
urlpatterns = [
    path('', views.home, name='home'),

    path('avaliable/', views.avaliable, name='avaliable'),

    path('add/', views.add, name='add'),

    path('borrow/', views.borrow, name='borrow'),

    path('borroweduser/', views.borroweduser, name='borroweduser'),

    path('borrowedadmin/', views.borrowedadmin, name='borrowedadmin'),

    path('edit/<int:book_id>/', views.edit, name='edit'),

    path('delete/<int:book_id>/', views.delete, name='delete'),

    path('password', views.password, name='password'),

    path('signup/', views.signup, name='signup'),

    path('login/', views.login, name='login'),

    path('book/<int:pk>/', views.detail, name='detail'),

    path('search/', views.search, name='search'),

    path('logout/', views.logout, name='logout'),

]
