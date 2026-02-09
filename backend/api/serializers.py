from models import Contribution, Contributor
from rest_framework import serializers


class ContributionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contribution
        fields = ["url", "contributor", "email", "contribution"]


class ContributorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contributor
        fields = ["zip_code", "full_name","employer"]
