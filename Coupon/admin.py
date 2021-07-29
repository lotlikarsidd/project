from django.contrib import admin
from .models import Coupon, Get, Vehicle, Location, View, CouponHandling

admin.site.register(Coupon)
admin.site.register(Get)
admin.site.register(Vehicle)
admin.site.register(Location)
admin.site.register(View)
admin.site.register(CouponHandling)