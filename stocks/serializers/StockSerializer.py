from rest_framework import serializers

class StockRequestSerializer(serializers.Serializer):
    symbol = serializers.CharField(max_length=10)