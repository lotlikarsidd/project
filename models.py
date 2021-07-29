from django.db import models
from datetime import date
from Login.models import Owner, Customer
from Coupon.models import Vehicle
from django.db.models.signals import pre_save, post_save

class Lend(models.Model):
    lid         = models.AutoField(primary_key=True)
    cid         = models.ForeignKey(Customer,on_delete=models.CASCADE)
    oid         = models.ForeignKey(Owner,on_delete=models.CASCADE)
    vid         = models.ForeignKey(Vehicle,on_delete=models.CASCADE)
    date_upload = models.DateField(auto_now_add=True) 
    date_of_return = models.DateField(blank=True,null=True)
    valid       = models.BooleanField(default=True)

    def __str__(self):
        return str(self.lid)

class Approval(models.Model):
    ap_id       = models.AutoField(primary_key=True)
    username    = models.CharField(max_length=100,blank=True,null=True)
    lid         = models.ForeignKey(Lend,on_delete=models.CASCADE)
    approve     = models.BooleanField(default=False)

    def __str__(self):
        return str(self.username) + ":" +str(self.approve)

class Car(models.Model):
    car_id      = models.AutoField(primary_key=True)
    vid         = models.ForeignKey(Vehicle,on_delete=models.CASCADE,blank=True,null=True)
    cnumber     = models.CharField(max_length=100,unique=True)
    seating_capacity = models.IntegerField()
    ctype       = models.CharField(max_length=100)
    cmodel      = models.CharField(max_length=100)
    cname       = models.CharField(max_length=100)
    crating     = models.FloatField()
    cprice      = models.FloatField()
    cimage      = models.FileField(blank=True,null=True)
    oid         = models.ForeignKey(Owner,on_delete=models.CASCADE)
    transmission= models.CharField(max_length=500,blank=True,null=True)
    description = models.TextField(max_length=1000,blank=True,null=True)
    updated		= models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cname) + "-:-" + str(self.oid.oname)


class Bike(models.Model):
    bike_id     = models.AutoField(primary_key=True)
    vid         = models.ForeignKey(Vehicle,on_delete=models.CASCADE,blank=True,null=True)
    bnumber     = models.CharField(max_length=100,unique=True)
    btype       = models.CharField(max_length=100,blank=True,null=True)
    bmodel      = models.CharField(max_length=100,blank=True,null=True)
    bname       = models.CharField(max_length=100,blank=True,null=True)
    brating     = models.FloatField(blank=True,null=True)
    bprice      = models.FloatField(blank=True,null=True)
    bimage      = models.FileField(max_length=100,blank=True,null=True)
    oid         = models.ForeignKey(Owner,on_delete=models.CASCADE)
    description = models.TextField(max_length=1000,blank=True,null=True)
    updated		= models.DateTimeField(auto_now=True)
    def __str__(self):
        return str(self.bname) + "-:-" + str(self.oid.oname)



def Vehicle_pre_save_receiver(sender,instance,*args,**kwargs):
    try:
        V = Vehicle(vtype=instance.cname)
        V.save()
        instance.vid = V
    except:
        V = Vehicle(vtype=instance.bname)
        V.save()

pre_save.connect(Vehicle_pre_save_receiver,sender=Car)
pre_save.connect(Vehicle_pre_save_receiver,sender=Bike)