from rest_framework import serializers
from datetime import datetime

class StockRequestSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=10)
    function = serializers.CharField(max_length=50, required=False)
    limit = serializers.IntegerField(required=False)
    interval = serializers.CharField(max_length=20, required=False)
    time_period = serializers.IntegerField(required=False, default=1)
    series_type = serializers.CharField(max_length=10, required=False)
    adjusted = serializers.BooleanField(required=False, default=True)
    extended_hours = serializers.BooleanField(required=False, default=True)
    month = serializers.CharField(max_length=10, required=False)
    outputsize = serializers.CharField(max_length=10, required=False)
    datatype = serializers.CharField(max_length=10, required=False)