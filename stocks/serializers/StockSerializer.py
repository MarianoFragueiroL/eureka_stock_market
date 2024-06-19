from rest_framework import serializers

class StockRequestSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=10)
    function = serializers.CharField(max_length=50, required=False)