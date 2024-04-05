from .models import Price, Registrator, ParseHistory
from rest_framework import serializers


class RegistratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registrator
        fields = "__all__"


class PriceSerializer(serializers.ModelSerializer):
    registrator = RegistratorSerializer(read_only=True)
    parse = serializers.PrimaryKeyRelatedField(queryset=ParseHistory.objects.all())

    class Meta:
        model = Price
        fields = "__all__"


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, label='Ваше Имя')
    contact = serializers.CharField(max_length=100, label='Телефон или email')
    speciality = serializers.CharField(max_length=100, label='Специальность')
    message = serializers.CharField(max_length=1000, label='Сообщение')

    class Meta:
        fields = "__all__"
