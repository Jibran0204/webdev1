from django.urls import path
from django.views.decorators.csrf import csrf_exempt


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("test", views.test, name="test") ,
    path("login_user", views.login_user, name="login"),
    path("check_login", views.check_login, name="check_login"),
    path("stories", views.stories, name="stories"),
    path("logout_user", views.logout_user, name="logout_user"),
    path("stories", views.storyManager, name="storyManager"),
    path('stories/<int:story_id>', views.delete_story, name='delete_story'),

]
