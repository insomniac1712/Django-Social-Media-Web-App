from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),

    # Global aliases (keep old template links working)
    path('login/', user_views.user_login, name='login'),
    path('password_reset', auth_view.PasswordResetView.as_view(
        template_name='users/password_reset_form.html'), name='password_reset'),
    path('password_reset/done', auth_view.PasswordResetDoneView.as_view(
        template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetConfirmView.as_view(),
        name='password_reset_complete'),
]