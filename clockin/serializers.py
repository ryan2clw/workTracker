from .models import IntervalWork
from invoice.models import Project
from django.contrib.auth.models import User
from rest_framework import serializers

class IntervalWorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = IntervalWork
        fields = ('user', 'started', 'finished', 'comments', 'project', 'id')

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ['name', 'id']
