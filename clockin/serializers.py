from .models import IntervalWork
from rest_framework import serializers

class IntervalWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntervalWork
        fields = ('user', 'started', 'finished', 'comments', 'project')
