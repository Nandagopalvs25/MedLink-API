from django.urls import path
from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView,UserDetailsView
from .views import PatientList,RecordView,UserProfileView,AiChatView,PostView,CommentView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="rest_register"),
    path("auth/login/", LoginView.as_view(), name="rest_login"),
    path("logout/", LogoutView.as_view(), name="rest_logout"),
    path("user/", UserDetailsView.as_view(), name="rest_user_details"),
    path("patients/", PatientList.as_view(), name="patients"),
    path("posts/", PostView.as_view(), name="post"),
    path("comment/", CommentView.as_view(), name="comment"),
    path("records/<int:id>/",RecordView.as_view(),name="patient_records"),
    path("records/",RecordView.as_view(),name="patient_records"),
    path("userProfile/",UserProfileView.as_view(),name='userprofile'),
    path("chat/",AiChatView.as_view(),name="patient_records"),

]