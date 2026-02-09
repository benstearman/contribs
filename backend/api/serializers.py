from .models import Contribution, Contributor
from rest_framework import serializers


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ["contributor", "committee", "amount", "receipt_date"]


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ["zip_code", "full_name", "employer"]
