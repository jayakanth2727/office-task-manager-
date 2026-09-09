from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, TaskCommentViewSet

router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')
router.register(r'comments', TaskCommentViewSet, basename='comment')

urlpatterns = router.urls