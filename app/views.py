# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.serializers import StudentSerializer
from app.models import Student


class StudentViews(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, id=None):

        if id:
            try:
                student = Student.objects.get(id=id)
            except Student.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)

            serializer = StudentSerializer(student)

            return Response(serializer.data, status=status.HTTP_200_OK)

        students = Student.objects.all()

        serializer = StudentSerializer(students, many=True)

        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request, id):

        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = StudentSerializer(student, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_200_OK)
