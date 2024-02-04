from django.shortcuts import get_object_or_404
import jwt
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, TaskUpdateSerializer
from django.http import Http404
from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from rest_framework import status



class UserTaskList(APIView):
    # permission_classes = [IsAuthenticated]

    def get_user_id_from_payload(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header or not authorization_header.startswith('Bearer '):
            return None

        token = authorization_header.split(' ')[1]

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            return payload.get('id')
        except jwt.ExpiredSignatureError:
            return None

    def get(self, request, format=None):
        user_id = self.get_user_id_from_payload(request)

        if not user_id:
            return Response({"detail": "Invalid token or user not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        user_tasks = Task.objects.filter(user=user_id)

        # Group tasks by status
        grouped_tasks = {
            'To Do': user_tasks.filter(status='Pending'),
            'In Progress': user_tasks.filter(status='In Progress'),
            'Completed': user_tasks.filter(status='Completed'),
        }

        serializer = {status: TaskSerializer(group, many=True).data for status, group in grouped_tasks.items()}
        return Response(serializer)

    def post(self, request, format=None):
        user_id = self.get_user_id_from_payload(request)

        if not user_id:
            return Response({"detail": "Invalid token or user not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        request.data['user'] = user_id

        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

class UserTaskDetails(APIView):
    # permission_classes = [IsAuthenticated]

    def get_user_id_from_payload(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header or not authorization_header.startswith('Bearer '):
            return None

        token = authorization_header.split(' ')[1]

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            return payload.get('id')
        except jwt.ExpiredSignatureError:
            return None

    def get(self, request, task_id, format=None):
        user_id = self.get_user_id_from_payload(request)

        if not user_id:
            return Response({"detail": "Invalid token or user not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        task = get_object_or_404(Task, id=task_id, user=user_id)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, task_id, format=None):
        user_id = self.get_user_id_from_payload(request)

        if not user_id:
            return Response({"detail": "Invalid token or user not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        task = get_object_or_404(Task, id=task_id, user=user_id)
        serializer = TaskUpdateSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id, format=None):
        user_id = self.get_user_id_from_payload(request)

        if not user_id:
            return Response({"detail": "Invalid token or user not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        task = get_object_or_404(Task, id=task_id, user=user_id)
        task.delete()
        return Response({"detail": "Task successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
    
class TaskSearch(APIView):

    def get_user_id_from_payload(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header or not authorization_header.startswith('Bearer '):
            return None

        token = authorization_header.split(' ')[1]

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            return payload.get('id')
        except jwt.ExpiredSignatureError:
            return None

    def get(self, request, format=None):
        user_id = self.get_user_id_from_payload(request)

        if not user_id:
            return Response({"detail": "Invalid token or user not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)

        user_tasks = Task.objects.filter(user=user_id)

        status_filter = request.query_params.get('status', None)
        title_filter = request.query_params.get('title', None)

        if status_filter:
            user_tasks = user_tasks.filter(status=status_filter)
        if title_filter:
            user_tasks = user_tasks.filter(title__icontains=title_filter)

        serializer = TaskSerializer(user_tasks, many=True)
        return Response(serializer.data)    


# Api's for normal crud operations

class TaskList(APIView):

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetail(APIView):
    """
    Retrieve, update, or delete a task instance.
    """
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    