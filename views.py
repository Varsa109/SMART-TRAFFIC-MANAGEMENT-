from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Student
from .serializers import StudentSerializer


class StudentViewSet(viewsets.ModelViewSet):
    """
    Provides the five CRUD endpoints for /api/students/:
      GET    /api/students/        -> list (supports ?search= and ?course= and ?status=)
      POST   /api/students/        -> create
      GET    /api/students/{id}/   -> retrieve
      PUT    /api/students/{id}/   -> full update
      PATCH  /api/students/{id}/   -> partial update
      DELETE /api/students/{id}/   -> delete
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        search = self.request.query_params.get("search")
        course = self.request.query_params.get("course")
        status_param = self.request.query_params.get("status")

        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(roll_no__icontains=search))
        if course:
            qs = qs.filter(course__iexact=course)
        if status_param:
            qs = qs.filter(status=status_param)
        return qs

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        name = instance.name
        self.perform_destroy(instance)
        return Response(
            {"detail": f"{name} removed from the register."},
            status=status.HTTP_200_OK,
        )
