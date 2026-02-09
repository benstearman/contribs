from .models import Contributor, Contribution
from rest_framework import permissions, viewsets

from .serializers import ContributionSerializer, ContributorSerializer


class ContributionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Contribution.objects.all().order_by("receipt_date")
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContributorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Contributor.objects.all().order_by("full_name")
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]