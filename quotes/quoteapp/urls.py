from django.urls import path
from . import views

app_name = 'quoteapp'

urlpatterns = [
    path('', views.main, name='main'),
    path('user/quote/', views.user_quotes, name='userquote'),
    path('author/', views.author, name='author'),
    path('quote/', views.quote, name='quote'),
    path('data/add_via_scrapping', views.add_via_scrapping, name='add_via_scrapping'),
    path('tag/', views.tag, name='tag'),
    path('tag/find/<int:tag_id>', views.find_quotes_by_tag, name='tag_find'),
    path('quote/user/find/<int:user_id>', views.find_quotes_by_user, name='user_find'),
    path('author_detail/<int:author_id>', views.author_detail, name='author_detail'),
    path('quote/edit/<int:quote_id>', views.quote_edit, name='quote_edit'),
    path('quote/delete/<int:quote_id>', views.quote_delete, name='quote_delete'),


]
