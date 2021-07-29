from rest_framework import serializers
from .models import Lend, Car, Bike

class LendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lend
        fields = ('lid',
                  'cid',
                  'oid',
                  'date_upload',)

class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('car_id',
                  'vid',
                  'cnumber',
                  'seating_capacity',
                  'ctype',
                  'cmodel',
                  'cname',
                  'crating',
                  'cprice',
                  'cimage',
                  'oid',
                  'transmission',
                  'description')

class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ('bike_id',
                  'vid',
                  'bnumber',
                  'btype',
                  'bmodel',
                  'bname',
                  'brating',
                  'bprice',
                  'bimage',
                  'oid',
                  'description')

