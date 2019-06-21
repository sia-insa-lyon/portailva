from django.conf.urls import url
from django.contrib.auth import views as auth_views

from portailva.member.forms import ResetPasswordForm
from portailva.member.views import PasswordUpdateView, ForgotPasswordView, LoginView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='member-login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='member-logout'),

    url(r'^forgot-password/$', ForgotPasswordView.as_view(), name='member-forgot-password'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z-]+)/$',
        auth_views.PasswordResetConfirmView.as_view(), {
            'template_name': 'member/password_reset.html',
            'post_reset_redirect': 'homepage',
            'form_class': ResetPasswordForm
         }, name='member-reset-password-confirm'),
    url(r'^change-password/$', PasswordUpdateView.as_view(), name='member-change-password')

]
