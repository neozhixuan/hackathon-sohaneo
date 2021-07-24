from django.urls import path

from . import views
app_name = "lifehack"
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<str:name>/profile", views.profile, name="profile"),
    path("<str:tutor>/tutorrequest", views.tutorrequest, name="tutorrequest"),
    path("accept", views.accept, name="accept"),
    path("classroom", views.classroom, name="classroom"),
    path("tuteemessage", views.tuteemessage, name="tuteemessage"),
    path("polldesign", views.polldesign, name = "polldesign"),
    path("create", views.create, name = "create"),
    path("canteen", views.canteen, name = "canteen"),
    path("like", views.like, name = "like"),
]
