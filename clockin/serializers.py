from .models import IntervalWork
from invoice.models import Project
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.utils.field_mapping import get_nested_relation_kwargs

class IntervalWorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = IntervalWork
        fields = ('user', 'started', 'finished', 'comments', 'project', 'id')

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        depth = 2
        model = Project
        fields = ['name', 'id', 'members']

    def build_nested_field(self, field_name, relation_info, nested_depth):
        """
        Create nested fields for forward and reverse relationships.
        """
        class NestedSerializer(serializers.ModelSerializer):
            class Meta:
                model = relation_info.related_model
                depth = nested_depth - 1
                fields = ['username','groups']

        field_class = NestedSerializer
        field_kwargs = get_nested_relation_kwargs(relation_info)

        return field_class, field_kwargs
