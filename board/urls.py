from django.urls import include, path
from . import views

app_name = 'Board'
urlpatterns = [
    path('', views.board, name='board'),
    path('<int:pk>', views.thread_view, name='thread'),
    path('<int:pk/comments>', views.CommentsView.as_view(), name='comments'),
    path('<int:pk/comment/post>', views.CommentView.as_view(), name='comment'),
    path('<int:pk>/thread/delete/', views.ThreadDelete.as_view(), name='delete_thread'),
    path('<int:pk>/comment/delete/', views.CommentDelete.as_view(), name='delete_comment'),
    path('user/', views.account, name='user'),
    path('user/<str:username>', views.guest, name='guest'),
]
