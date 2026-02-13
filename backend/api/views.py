from .models import Contributor, Contribution
from rest_framework import permissions, viewsets

from .serializers import ContributionSerializer, ContributorSerializer


class ContributionViewSet(viewsets.ModelViewSet):
    # This change reduces 100+ database hits to just 1
    queryset = Contribution.objects.select_related('contributor', 'committee').all().order_by("receipt_date")
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContributorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Contributor.objects.all().order_by("full_name")
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]