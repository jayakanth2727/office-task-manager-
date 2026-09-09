from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Task, TaskComment, Profile
from .serializers import TaskSerializer, TaskCommentSerializer


def is_admin(user):
    return hasattr(user, 'profile') and user.profile.role == 'admin'


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'priority', 'assigned_to']
    search_fields = ['title']

    def get_queryset(self):
        user = self.request.user
        if is_admin(user):
            return Task.objects.all().order_by('-created_at')
        # Employees only see their own tasks
        return Task.objects.filter(assigned_to=user).order_by('-created_at')

    def perform_create(self, serializer):
        # Only admins should reach here in practice; enforced in has_permission too
        serializer.save()

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        user = request.user
        qs = Task.objects.all() if is_admin(user) else Task.objects.filter(assigned_to=user)
        today = timezone.now().date()
        data = {
            'total': qs.count(),
            'pending': qs.filter(status='Pending').count(),
            'in_progress': qs.filter(status='In Progress').count(),
            'completed': qs.filter(status='Completed').count(),
            'overdue': qs.filter(due_date__lt=today).exclude(status='Completed').count(),
        }
        return Response(data)


class TaskCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if is_admin(user):
            return TaskComment.objects.all()
        return TaskComment.objects.filter(task__assigned_to=user)

    def perform_create(self, serializer):
        task = serializer.validated_data['task']
        user = self.request.user
        # Security: employee can only comment on their OWN task
        if not is_admin(user) and task.assigned_to != user:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You cannot comment on a task that isn't yours.")
        serializer.save(author=user)
