from rest_framework import serializers

class StockRequestSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=10)
    function = serializers.CharField(max_length=50, required=False)
    interval = serializers.CharField(max_length=20, required=False)
    time_period = serializers.IntegerField(required=False)
    series_type = serializers.CharField(max_length=10, required=False)