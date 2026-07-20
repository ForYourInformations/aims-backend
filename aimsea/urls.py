from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('admin/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('admin/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('admin/', admin.site.urls),
    path('api/', include('main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
path('admin/password_reset/', 
    auth_views.PasswordResetView.as_view(
        template_name='admin/password_reset_form.html',
        email_template_name='admin/password_reset_email.html',
        subject_template_name='admin/password_reset_subject.txt',
    ), 
    name='admin_password_reset'),

path('admin/password_reset/done/', 
    auth_views.PasswordResetDoneView.as_view(
        template_name='admin/password_reset_done.html',
    ), 
    name='password_reset_done'),

path('admin/reset/<uidb64>/<token>/', 
    auth_views.PasswordResetConfirmView.as_view(
        template_name='admin/password_reset_confirm.html',
    ), 
    name='password_reset_confirm'),

path('admin/reset/done/', 
    auth_views.PasswordResetCompleteView.as_view(
        template_name='admin/password_reset_complete.html',
    ), 
    name='password_reset_complete'),