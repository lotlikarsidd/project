from django.conf.urls import url
from .models import Lend, Car, Bike
from .views import NotificationViewLendReject, NotificationViewLendApprove,NotificationViewLend,insert_bike,CarsDetailView,BookVehicleQBike,ModelFormUpdateViewLend,CustomerDashboard,BookVehicleBike,BookVehicleQCar,BookVehicleCar,ViewDashboardCar,ViewDashboardBike, CarList, BikesDetailView, BikeList, ModelFormCreateViewCar,ModelFormCreateViewBike,ModelFormUpdateViewBike,ModelFormUpdateViewCar,ModelFormUpdateViewOwner,ModelFormUpdateViewCustomer,Dashboard,CarDeleteView,BikeDeleteView,DeleteDashboardCar,DeleteDashboardBike
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
    path('car/', CarList.as_view(), name='CarList'),
    path('car/<int:pk>/',CarsDetailView.as_view()),
    path('car/add/', ModelFormCreateViewCar.as_view(), name='create'),
    path('car/update/<int:pk>/', ModelFormUpdateViewCar.as_view(), name='update'),
    path('bike/', BikeList.as_view(), name='bikelist'),
    path('bike/<int:pk>/',BikesDetailView.as_view()),
    path('bike/add', ModelFormCreateViewBike.as_view(), name='create'),
    path('owner/update/<int:pk>', ModelFormUpdateViewOwner.as_view()),
    path('customer/update/<int:pk>', ModelFormUpdateViewCustomer.as_view()),
    
    path('bike/update/<int:pk>/', ModelFormUpdateViewBike.as_view(), ),
    path('lend/dashboard/', Dashboard.as_view()),
    path('lend/customer/dashboard/', CustomerDashboard.as_view()),
    path('lend/viewcar/', ViewDashboardCar.as_view()),
    path('lend/viewbike/', ViewDashboardBike.as_view()),
    path('lend/deletecar/', DeleteDashboardCar.as_view()),
    path('lend/deletebike/', DeleteDashboardBike.as_view()),
    path('bike/delete/<int:pk>/', BikeDeleteView.as_view() ),
    path('car/delete/<int:pk>/', CarDeleteView.as_view() ),
    path('lend/request/submit/<int:pk>/', BookVehicleBike.as_view() ),
    path('lend/request/submit/question/<int:pk>/', BookVehicleQBike.as_view() ),
    path('lend/car/request/submit/<int:pk>/', BookVehicleCar.as_view() ),
    path('lend/car/request/submit/question/<int:pk>/', BookVehicleQCar.as_view() ),
    path('lend/update/<int:pk>/', ModelFormUpdateViewLend.as_view(), ),
    path('lend/inform/', NotificationViewLend.as_view(), ),
    path('lend/inform/approve/<int:pk>/', NotificationViewLendApprove.as_view(), ),
    path('lend/inform/reject/<int:pk>/', NotificationViewLendReject.as_view(), ),
    # path('lend/',LendApi),
    # path('lend/<int:id>/',LendApi),

    # path('bike/',BikeApi),
    # path('bike/<int:id>/',BikeApi),
    # path('car/<slug:slug>/',CarApi),
    # path('bike/insert/',insert_bike),
    # path('bike/',BikeApi),
    # path('car/<int:id>/',CarApi),
    # path('car/<slug:slug>/',CarApi),
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)