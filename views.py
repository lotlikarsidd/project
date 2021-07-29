from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, logout
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.views.generic import ListView,DetailView,TemplateView, CreateView
from .serializers import RegistrationSerializer, AccountPropertiesSerializer, ChangePasswordSerializer
from account.models import Account
from urllib.parse import urlparse, urlunparse
from django.utils import timezone
import datetime
import random
from time import sleep
from django.conf import settings
# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm,
)
from Coupon.models import CouponHandling,Coupon,Get
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from Login.models import Login,Customer
from Rent.models import Tourist,Hotel
from Lend.models import Car,Bike
from rest_framework.authtoken.models import Token
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from account.forms import CustomFormCreate, CustomAuthCreate
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import get_user_model, login
from Login.models import Login, Owner
from Lend.models import Car, Bike,Lend
from django.urls import reverse
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes



def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			print(associated_users)
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "registration/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="registration/password_reset.html", context={"password_reset_form":password_reset_form})

User = get_user_model()

def validate_email(email):
	account = None
	try:
		account = Account.objects.get(email=email)
	except Account.DoesNotExist:
		return None
	if account != None:
		return email

def validate_username(username):
	account = None
	try:
		account = Account.objects.get(username=username)
	except Account.DoesNotExist:
		return None
	if account != None:
		return username





		


def SignupView(request):
    if request.method == 'POST':
        form = CustomFormCreate(request.POST)
        if form.is_valid():
        	form.save()
        	username = form.cleaned_data.get('username')
        	email = form.cleaned_data.get('email')
        	raw_password = form.cleaned_data.get('password')
        	# user = authenticate(username=email, password=raw_password)
        	# login(request, user)
        	return redirect('home')
    else:
        form = CustomFormCreate()
    return render(request, 'signup.html', {'form': form})

class AboutView(TemplateView):
	template_name = "pwa/about.html"

class ContactView(TemplateView):
	template_name = "pwa/aboutus.html"



def view(request):
	if request.user.is_authenticated: 
		if request.user.is_owner:
			return HttpResponseRedirect("/Lend/lend/dashboard/")
		else:
			return HttpResponseRedirect("/home")

class SuccessURLAllowedHostsMixin:
    success_url_allowed_hosts = set()

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}

class LoginView(SuccessURLAllowedHostsMixin, FormView):
    """
    Display the login form and handle the login action.
    """
    form_class = CustomAuthCreate
    authentication_form = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'registration/login.html'
    redirect_authenticated_user = False
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)


    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""

        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs() 
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        # L = Login.objects.filter(username=request.user.username).update(timestamp_logout = datetime.datetime.now(tz=timezone.utc))
	# L1 = Login.objects.filter(username=request.user.username).update(total_usage = timestamp_logout - timestamp_login)
	# print(L1)
        
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        return context

    def get_success_url(self):
        U = CouponHandling.objects.get(username=self.request.user.username)	
        U.user = self.request.user.username
        U.timestamp_login = datetime.datetime.now(timezone.utc)
        U.save()
       	U = CouponHandling.objects.all().first()
       	print("U.user",U.user,U.timestamp_login)
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)


def LogoutView(request):
	U = CouponHandling.objects.get(username=request.user.username)	
	U.timestamp_logout = datetime.datetime.now(timezone.utc)
	datetime1 = U.timestamp_logout
	datetime2 = U.timestamp_login
	if not U.total_usage :
		U.total_usage = str(datetime1 - datetime2)

	else:
		print('U.total_usage',U.total_usage)
		print('U.total_usage :',str(datetime1 - datetime2))
		a,b,c=str(U.total_usage).split(":")
		print(a,b,c)
		try:
			x,y,z=(str(datetime1 - datetime2)).split(":")
		except:
			return redirect('home')
		print(x,y,z)
		a = int(a);b = int(b);x = int(x);y = int(y);
		print(int(a+x),int(int(b)+int(y)),0)
		p = int(a+x)
		q = int(b+y)
		if q >= 60:
			p = p + 1
			q = q - 60
		U.total_usage = datetime.time(p,q,0)
		if p >=1 and q>=40:
			G = Get.objects.get(username=request.user.username)
			G.coup_id = Coupon.objects.get(coup_id=2)
			G.coupon_unique_code = 'coup'+str(random.randint(1111111,9999999))
			print(G)
			G.save()
	U.save()
	print('U.total_usage',U.total_usage)
	logout(request)
	context={}
	return redirect('home')



class HomeView(TemplateView):
	template_name = "pwa/new.html"

	def get_context_data(self,*args,**kwargs):
		# if self.request.user.is_authenticated:
		# 	A = None
		# 	if self.request.user.is_owner:
		# 		O = Owner.objects.all().filter(oname=self.request.user.username)
		# 		A = Lend.objects.all().filter(oid=O)
		# 	else:
		# 		O = Customer.objects.all().filter(cname=self.request.user.username)
		# 		A = Lend.objects.filter(cid=O)
		# 	List = []
		# 	L = None
		# 	print(A)
		# 	for lender in A:
		# 		L = Approval.objects.filter(lid=lender).filter(approve=True)
		# 		if L:
		# 			List.append(lender)
		# 	for ob in List:
		# 		x = ob.date_of_return - date.today()
		# 		print(x)
		# 		if x.days <= 0:
		# 			ob.valid = False
		# 			ob.save()
		CarCount = Car.objects.all().count()
		BikeCount = Bike.objects.all().count()
		LoginCount = Login.objects.all().count()
		TouristCount = Tourist.objects.all().count()
		context = super().get_context_data(*args,**kwargs)
		context['CarCount'] = CarCount
		context['BikeCount'] = BikeCount
		context['LoginCount'] = LoginCount
		context['TouristCount'] = TouristCount
		context['objc'] = Car.objects.all()[:5]
		context['objb'] = Bike.objects.all()[:5]
		if self.request.user.is_authenticated:
			context['user'] = self.request.user
			context['check'] = True
		else:
			context['check'] = False
        
		print(context)
		return context