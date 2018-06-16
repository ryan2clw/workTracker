from rest_framework import serializers
from clockin.models import Bill

class BillSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bill
        fields = ('customer','project','created','pay_rate','tax')

