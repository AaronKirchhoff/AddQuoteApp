from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('user/create', views.create),
    path('results/', views.results),
    path('user/login', views.login),
    path('quote/create', views.new_quote),
    path('quote/<int:id>', views.author_page),	  
    path('like_quote/<int:id>', views.like_quote), 
    path('quote/<int:id>/delete', views.delete),
    path('logout/', views.logout),
    path('account_edit/', views.edit),
    path('this_quote/<int:id>', views.this_quote),
    path('user/<int:id>/update/', views.update),

]