from rest_framework import serializers
from app.models import Student


class StudentSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    date_of_birth = serializers.DateField()
    grade = serializers.IntegerField()
    phone = serializers.CharField(max_length=100)
    email = serializers.CharField(max_length=100)

    class Meta:
        model = Student
        fields = ('__all__')