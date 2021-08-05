
from django.urls import path 
from rango import views

app_name = 'rango'

urlpatterns = [ 
    path('', views.index, name='index'), 
    path('about/',views.about,name='about'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('add_category/', views.add_category, name='add_category'),
    path('category/<slug:category_name_slug>/add_page/',views.add_page,name='add_page'),
    path('register/',views.register,name='register'),
    path('login/',views.user_login,name='login'),
    path('restricted/',views.restricted,name='restricted'),
    path('logout/',views.user_logout,name='logout'),
    path('<slug:category_name_slug>/<slug:page_title_slug>',views.show_page,name='show_page'),
    path('<slug:category_name_slug>/<slug:page_title_slug>/add_comment/',views.add_comment,name='add_comment'),
    path('like_page/', views.like_page, name="like_page"),
    path('mark_page/',views.mark_page, name="mark_page"),
    path('profile/',views.profile, name="profile_page"),
    path('update_profile/',views.update_profile, name="update_profile"),
    path('marklist/',views.marklist, name="marklist"),
    path('likelist/',views.likelist, name="likelist"),
    path('commentlist/',views.commentlist, name="commentlist"),
    path('deletecomment/',views.deletecomment,name="deletecomment"),
    path('deletelike/',views.deletelike,name="deletelike"),
    path('deletemark/',views.deletemark,name="deletemark"),
]
