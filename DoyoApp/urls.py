from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from account.views import ContactView,password_reset_request,HomeView, LogoutView, SignupView, view,AboutView, LoginView
urlpatterns = [
    
    path('',HomeView.as_view(),name='home'),
    path("",include('pwa.urls')),
	path('home/',HomeView.as_view(),name='home'),
    path('accounts/profile/',view,name='view'),
    path('login/', LoginView.as_view(),name="login"),
    path('signup/', SignupView,name="signup"),
    path('logout', LogoutView,name="logout"),
    path('admin/', admin.site.urls),
    path("password_reset/", password_reset_request, name="password_reset_form"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),      

    path('Login/', include('Login.urls')),
    path('Test/',include('Test.urls')),
    path('Lend/',include('Lend.urls')),
    path('Rent/',include('Rent.urls')),
    path('Coupon/',include('Coupon.urls')),
    path('api/', include('account.urls')),
    path('about/', AboutView.as_view(),name='about'),
    path('Contact/', ContactView.as_view(),name='Contact'),
    # path('services/', include('account.urls')),
    path('services/',RedirectView.as_view(url='http://127.0.0.1:8001/')),
] 
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)