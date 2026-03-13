from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import Contributor, Contribution, Candidate, Committee, Party
from .serializers import (
    ContributionSerializer, 
    ContributorSerializer, 
    CandidateSerializer, 
    CommitteeSerializer, 
    PartySerializer
)

class PartyViewSet(viewsets.ReadOnlyModelViewSet):
    """View political party codes and names."""
    queryset = Party.objects.all().order_by('id')
    serializer_class = PartySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CandidateViewSet(viewsets.ModelViewSet):
    """View and edit candidate details."""
    # select_related avoids extra queries for the party name
    queryset = Candidate.objects.select_related('CAND_PTY_AFFILIATION').all().order_by("CAND_NAME")
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'])
    def committees(self, request, pk=None):
        candidate = self.get_object() # Finds the specific candidate
        committees = candidate.committees.all() # Grabs their committees
        serializer = CommitteeSerializer(committees, many=True)
        return Response(serializer.data)
    
class CommitteeViewSet(viewsets.ModelViewSet):
    """View and edit committee details."""
    # select_related avoids extra queries for the supported candidate
    queryset = Committee.objects.select_related('CAND_ID').all().order_by("CMTE_NM")
    serializer_class = CommitteeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ContributionViewSet(viewsets.ModelViewSet):
    """View and edit individual contributions."""
    # Optimizes deep joins for nested detail fields in the serializer
    queryset = Contribution.objects.select_related(
        'contributor', 
        'committee', 
        'committee__CAND_ID'
    ).all().order_by("-receipt_date")
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ContributorViewSet(viewsets.ModelViewSet):
    """View and edit contributor profiles."""
    queryset = Contributor.objects.select_related('employer').all().order_by("full_name")
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]