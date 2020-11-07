from rest_framework import serializers
from tracker.models import Show


class ShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Show
        fields = ('show_name', 'overview', 'kind', 'year', 'service')
