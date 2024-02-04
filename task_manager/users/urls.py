from django.urls import path
from .views import CustomUserCreate, LoginView, PasswordReset, UserView, LogoutView, GetUserById
app_name = 'users'

urlpatterns = [
    path('', CustomUserCreate.as_view(), name="users"),
    path('<int:user_id>/', GetUserById.as_view(), name='user-detail'),
    path('login/', LoginView.as_view(), name="login_user"),
    path('logout/', LogoutView.as_view(), name="logout_user"),
    path('me/', UserView.as_view(), name="user"),
    path('reset-password/<int:user_id>/', PasswordReset.as_view(), name='reset-password'),

]
