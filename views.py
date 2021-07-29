from django.shortcuts import render
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from .models import Lend, Car, Bike, Approval
from django.http.response import JsonResponse
from Login.models import Owner, Customer
from .serializers import LendSerializer, CarSerializer, BikeSerializer
from django.core.files.storage import default_storage
from django.shortcuts import render, redirect, reverse
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView, View
from .forms import CarModelForm,LendModelForm, BikeModelForm, OwnerModelForm, CustomerModelForm
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import default_storage
import csv
import json
from Coupon.models import Vehicle


            
class CarsDetailView(DetailView):
    model = Car
    # form_class = CarModelForm
    template_name = 'cars/car_detail.html'



            
class BikesDetailView(DetailView):
    model = Bike
    template_name = 'bikes/bike_detail.html'

    def image_view(self):
        if self.bimage:
            return True



class ModelFormCreateViewBike(CreateView):
    form_class = BikeModelForm
    template_name = 'bikes/forms_bike.html'
    success_url = '/Lend/lend/dashboard/'
    login_url = '/login'

    def form_valid(self,form):
        instance = form.save(commit=False)
        instance.bimage = self.request.FILES.get('bimage')
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)

    def get_context_data(self):
        context = super(ModelFormCreateViewBike,self).get_context_data()
        context['type_op'] = 'Create'
        context['type'] = 'Car'
        context['is_Car'] = True
        return context
    def form_invalid(self,form):
        return redirect('/Lend/lend/dashboard/')

class ModelFormUpdateViewCar(UpdateView):
    form_class = CarModelForm
    template_name = 'cars/forms_car.html'
    success_url = '/Lend/lend/viewcar/'
    login_url = '/login'

    def get_context_data(self):
        context = super(ModelFormUpdateViewCar,self).get_context_data()
        context['type_op'] = 'Update'
        context['type'] = self.get_object().cname
        return context
    def form_invalid(self,form):
        return redirect('/Lend/lend/viewcar/')

    def get_queryset(self):
        return Car.objects.all()



class ViewDashboardCar(TemplateView):
    template_name = 'profile/view.html'
    def get_context_data(self):
        obj = Owner.objects.filter(oemail=self.request.user.email).first()
        cobj = Car.objects.filter(oid=obj.oid)
        print(cobj)
        context={'obj':cobj,'type':'Cars Lend','car':True}
        return context
    
class ViewDashboardBike(TemplateView):
    template_name = 'profile/view.html'
    def get_context_data(self):
        obj = Owner.objects.filter(oemail=self.request.user.email).first()
        oobj = Bike.objects.filter(oid=obj.oid)
        print(oobj)
        context={'obj':oobj,'type':'Bikes Lend','car':False}
        return context
    
class DeleteDashboardCar(TemplateView):
    template_name = 'profile/view.html'
    def get_context_data(self):
        obj = Owner.objects.filter(oemail=self.request.user.email).first()
        cobj = Car.objects.filter(oid=obj.oid)
        print(cobj)
        context={'obj':cobj,'type':'Cars Lend','car':True,'delete':True}
        return context
    
class DeleteDashboardBike(TemplateView):
    template_name = 'profile/view.html'
    def get_context_data(self):
        obj = Owner.objects.filter(oemail=self.request.user.email).first()
        oobj = Bike.objects.filter(oid=obj.oid)
        print(oobj)
        context={'obj':oobj,'type':'Bikes Lend','car':False,'delete':True}
        return context
    

class Dashboard(TemplateView):
    template_name = 'profile/owner.html'
    def get_context_data(self):
        obj = Owner.objects.filter(oemail=self.request.user.email).first()
        objo = Owner.objects.filter(oemail=self.request.user.email).first().oid
        print(self.request.user.username)
        A = Lend.objects.filter(oid=objo)
        L = None
        List = []
        for lend in A:
            L = Approval.objects.filter(lid=lend,approve=True)
            if L:
                List.append(lend)
        for ob in List:
            x = ob.date_of_return - date.today()
            print(x)
            if x.days <= 0:
                ob.valid = False
                ob.save()
        context={'obj':obj,'id':123,'owner':True,'L':List}
        return context

class CustomerDashboard(TemplateView):
    template_name = 'profile/owner.html'
    def get_context_data(self):
        obj = Customer.objects.filter(cemail=self.request.user.email).first()
        objc = Customer.objects.filter(cemail=self.request.user.email).first().cid
        print(self.request.user.username)
        A = Lend.objects.filter(cid=objc)
        List = []
        L = None
        for lend in A:
            L = Approval.objects.filter(lid=lend,approve=True)
            if L:
                List.append(lend)
        for ob in List:
            x = ob.date_of_return - date.today()
            print(x)
            if x.days <= 0:
                ob.valid = False
                ob.save()
        # date_q = L.date_upload - L.date_of_return
        print(L)
        context={'obj':obj,'id':123,'owner':False,'L':List}
        return context

    def dateCalc(self):
        return (self.date_of_return - date.today()).days
    def status(self):
        if not self.valid:
            return False
        else:
            return True


class ModelFormUpdateViewCustomer(LoginRequiredMixin,UpdateView):
    form_class = CustomerModelForm
    template_name = 'profile/forms.html'
    success_url = '/Lend/lend/customer/dashboard/'
    login_url = '/login'

    def get_context_data(self):
        context = super(ModelFormUpdateViewCustomer,self).get_context_data()
        context['type_op'] = 'Update'
        context['type'] = 'Customer'
        return context
    def form_invalid(self,form):
        return redirect('/Lend/lend/customer/dashboard/')

    def get_queryset(self):
        return Customer.objects.all()

class ModelFormUpdateViewOwner(LoginRequiredMixin,UpdateView):
    form_class = OwnerModelForm
    template_name = 'profile/forms.html'
    success_url = '/Lend/lend/dashboard/'
    login_url = '/login'
    def get_context_data(self):
        context = super(ModelFormUpdateViewOwner,self).get_context_data()
        context['type_op'] = 'Update'
        context['type'] = 'Owner'
        return context
    def form_invalid(self,form):
        return redirect('/Lend/lend/dashboard/')

    def get_queryset(self):
        return Owner.objects.all()



class CarDeleteView(DeleteView):
    model = Car
    success_url ="/Lend/lend/deletecar/"

class BikeDeleteView(DeleteView):
    model = Bike
    success_url ="/Lend/lend/deletebike/"

class BookVehicleBike(LoginRequiredMixin,TemplateView):
    template_name = 'profile/book.html'

    def get_context_data(self,pk,*args):
        print(pk)
        B = Bike.objects.filter(bike_id=pk).first()
        print(B.bname)
        O=B.oid
        print(self.request.POST.get('question'))
        context={'objb':B,'objo':O,'bike':True}
        return context
class BookVehicleCar(LoginRequiredMixin,TemplateView):
    template_name = 'profile/book.html'

    def get_context_data(self,pk,*args):
        print(pk)
        B = Car.objects.filter(car_id=pk).first()
        print(B.cname)
        O=B.oid
        print(self.request.POST.get('question'))
        context={'objb':B,'objo':O,'bike':False}
        return context
class ModelFormUpdateViewLend(LoginRequiredMixin,UpdateView):
    form_class = LendModelForm
    template_name = 'profile/forms.html'
    success_url = '/Lend/lend/customer/dashboard/'
    login_url = '/login'
    def get_context_data(self):
        context = super(ModelFormUpdateViewLend,self).get_context_data()
        context['type_op'] = 'Update'
        context['type'] = 'Customer'
        return context

    def form_invalid(self,form):
        return redirect('/Lend/customer/lend/dashboard/')

    def get_queryset(self):
        return Lend.objects.all()
class NotificationViewLendApprove(LoginRequiredMixin,TemplateView):
    template_name = 'profile/view.html'

    def get_context_data(self,pk):
        context = {}
        z = True
        if self.request.user.is_owner:
            O = Approval.objects.get(ap_id=pk)
            O.approve = True
            O.save()
            A = Approval.objects.filter(username=self.request.user.username,approve=False)
            
    
            C = Customer.objects.filter(cemail=self.request.user.email).first()
            context = { 'obj':A,'z':z}
        return context

class NotificationViewLendReject(LoginRequiredMixin,TemplateView):
    template_name = 'profile/view.html'

    def get_context_data(self,pk):
        context = {}
        z = True
        if self.request.user.is_owner:
            O = Approval.objects.get(ap_id=pk)
            O.delete()
            A = Approval.objects.filter(username=self.request.user.username,approve=False)
            
    
            C = Customer.objects.filter(cemail=self.request.user.email).first()
            context = { 'obj':A,'z':z}
        return context
class NotificationViewLend(LoginRequiredMixin,TemplateView):
    template_name = 'profile/view.html'

    def get_context_data(self):
        context = {}
        z = True
        if self.request.user.is_owner:
            A = Approval.objects.filter(username=self.request.user.username,approve=False)
            C = Customer.objects.filter(cemail=self.request.user.email).first()
            context = { 'obj':A,'z':z}
        return context

class BookVehicleQBike(LoginRequiredMixin,TemplateView):
    template_name = 'profile/book.html'

    def get_context_data(self,pk):
        B = Bike.objects.filter(bike_id=pk).first()
        O = B.oid
        C = Customer.objects.filter(cemail=self.request.user.email).first()
        print(C)
        print(O)
        print(B.vid)
        le = Lend.objects.filter(vid=B.vid,valid=True).count()
        a = ""
        if le > 0:
            q = False
            p = True
        else:
            q = True
            p = False
            print(C)
            L = Lend(cid=C,oid=O,vid=B.vid)
            print(L.lid)
            L.save()
            A = Approval(lid=L,username=L.oid.oname)
            A.save()
            a = str(L.lid)
        context={'q':q,'p':p,'objb':B,'objo':O,'bike':True,'lid':a}
        return context
class BookVehicleQCar(LoginRequiredMixin,TemplateView):
    template_name = 'profile/book.html'

    def get_context_data(self,pk):
        B = Car.objects.filter(car_id=pk).first()
        O = B.oid
        C = Customer.objects.filter(cemail=self.request.user.email).first()
        print(C)
        print(O)
        print(B.vid)
        le = Lend.objects.filter(vid=B.vid).count()
        a = ""
        if le > 0:
            q = False
            p = True
        else:
            q = True
            p = False
            L = Lend(cid=C,oid=O,vid=B.vid)
            print(L.lid)
            L.save()
            A = Approval(lid=L,username=L.oid.oname)
            A.save()
            a = str(L.lid)
        context={'q':q,'p':p,'objb':B,'objo':O,'bike':False,'lid':a}
        return context

def insert_bike(request,id=0):
    csvFilePath = staticfiles_storage.path('bike_lend.csv')
    
    print(csvFilePath)
    data = {}
    O = Owner.objects.all().first()
    # Open a csv reader called DictReader
    with open(csvFilePath) as csvf:
        csvReader = csv.DictReader(csvf)

        for rows in csvReader:
            V = Vehicle.objects.filter(vid=rows['vid_id']).first()
        
            _, created = Bike.objects.get_or_create(
    bike_id      = rows['bike_id'],
    vid         = V, 
    bnumber     = rows['bnumber'], 
    btype       = rows['btype'], 
    bmodel      = rows['bmodel'], 
    bname       = rows['bname'], 
    brating     = rows['brating'], 
    bprice      = rows['bprice'], 
    bimage      = rows['bimage'], 
    oid        = O, 
    description = rows['description'], 
    slug		= rows['slug']

            )
        return JsonResponse("Added Successfully!!" , safe=False)





class ModelFormUpdateViewBike(LoginRequiredMixin,UpdateView):
    form_class = BikeModelForm
    template_name = 'bikes/forms_bike.html'
    success_url = '/Lend/lend/viewbike/'
    login_url = '/login'
    def get_context_data(self,*args,**kwargs):
        context = super(ModelFormUpdateViewBike,self).get_context_data()
        context['type_op'] = 'Update'
        context['type'] = self.get_object().bname
        return context
    def get_queryset(self):
        return Bike.objects.all()
    def form_invalid(self):
        return redirect('/Lend/lend/viewbike/')
    
class ModelFormCreateViewCar(CreateView):
    form_class = CarModelForm
    template_name = 'cars/forms_car.html'
    success_url = '/Lend/lend/dashboard/'
    login_url = '/login'

    def form_valid(self,form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return super().form_valid(form)
    def form_invalid(self):
        return redirect('/Lend/lend/dashboard/')


class CarList(ListView):
    template_name = 'cars/car_list.html'
    def get_queryset(self):
        print(self.request.GET)
        return Car.objects.all()
    def get_context_data(self):
        context = {}
        
        print(self.request.GET.get('sort'))
        if self.request.GET.get('searchsort') == '1':
            search = self.request.GET.get('search')
            C = Car.objects.all().filter(Q(cname__contains=search)|
            Q(cmodel__contains=search)|
            Q(ctype__contains=search)|
            Q(description__contains=search)
            )
            context['object_list'] = C
        elif self.request.GET.get('sort') == '1':
            if self.request.GET.get('sort1') == '1':
                context['object_list'] = Car.objects.order_by('cprice')
            else:
                context['object_list'] = Car.objects.order_by('crating')
        elif self.request.GET.get('sort') == '0': 
            if not self.request.GET.get('sort1') == '1':
                context['object_list'] = Car.objects.order_by('-crating')
            else:
                context['object_list'] = Car.objects.order_by('-cprice')
        else:
            context['object_list'] = Car.objects.all()
        return context


class BikeList(ListView):
    template_name = 'bikes/bike_list.html'

    def get_queryset(self):
        print(self.request.GET)
        return Bike.objects.all()
    def get_context_data(self):
        context = {}
        # context['object_list'] = Bike.objects.all()
        print(self.request.GET.get('sort'))
        if self.request.GET.get('searchsort') == '1':
            search = self.request.GET.get('search')
            context['object_list'] = Bike.objects.all().filter(Q(bname__contains=search)|
            Q(bmodel__contains=search)|
            Q(btype__contains=search)|
            Q(description__contains=search)
            )
        elif self.request.GET.get('sort') == '1':
            if self.request.GET.get('sort1') == '1':
                context['object_list'] = Bike.objects.order_by('bprice')
            else:
                context['object_list'] = Bike.objects.order_by('brating')
        elif self.request.GET.get('sort') == '0':
            if not self.request.GET.get('sort1') == '1':
                context['object_list'] = Bike.objects.order_by('-brating')
            else:
                context['object_list'] = Bike.objects.order_by('-bprice')
        else:
            context['object_list'] = Bike.objects.all()
        
        return context