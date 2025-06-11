from django.urls import path
from challenge.core.views import ChangePasswordView, LoginView, ResetPassword, RequestPasswordReset, SignUpView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('request-password-reset/', RequestPasswordReset.as_view(), name='password_reset'),
    path('reset-password/<str:token>/', ResetPassword.as_view(), name='password_confirm'),
]
