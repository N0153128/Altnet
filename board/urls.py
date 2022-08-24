from django.urls import path
from . import views

app_name = 'Board'
urlpatterns = [
    path('', views.board, name='board'),
    path('<int:pk>', views.thread_view, name='thread'),
    path('<int:pk>/comments', views.CommentsView.as_view(), name='comments'),
    path('<int:pk>/comment/post', views.CommentView.as_view(), name='comment'),
    path('user/', views.account, name='user'),
    path('user/<str:username>', views.guest, name='guest'),
    path('category/<str:cat>', views.category, name='cat'),
    path('user/message/<int:pk>/delete', views.message_remove, name='delete_message'),
    path('<int:pk>/thread/delete/', views.thread_remove, name='delete_thread'),
    path('<int:pk>/comment/delete/', views.comment_remove, name='delete_comment'),
]