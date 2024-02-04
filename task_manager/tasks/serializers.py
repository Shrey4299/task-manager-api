from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status']

    def validate(self, data):
        """
        Validate that at least one field is provided for updating.
        """
        if not any(data.values()):
            raise serializers.ValidationError("At least one field is required for updating.")
        return data
