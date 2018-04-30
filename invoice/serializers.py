from .models import Project
from rest_framework import serializers

class ProjectHoursSerializer(serializers.ModelSerializer):

	intervals = serializers.RelatedField(many=True)

    class Meta:
        model = Project
        fields = ('name', 'user', 'intervals')
