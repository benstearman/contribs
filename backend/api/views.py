from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import Contributor, Contribution, Candidate, Committee, Party, Employer
from rest_framework.views import APIView
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
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    filter_backends = [filters.SearchFilter]
    search_fields = ['CAND_NAME']

    def get_queryset(self):
        queryset = Candidate.objects.select_related('CAND_PTY_AFFILIATION').all().order_by("CAND_NAME")
        
        # Manual filtering for Election list navigation
        state = self.request.query_params.get('state')
        office = self.request.query_params.get('office')
        year = self.request.query_params.get('year')
        
        if state:
            queryset = queryset.filter(CAND_OFFICE_ST=state)
        if office:
            queryset = queryset.filter(CAND_OFFICE=office)
        if year:
            queryset = queryset.filter(CAND_ELECTION_YR=year)
            
        return queryset

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

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ElectionSummaryView(APIView):
    """Calculates top contributors and employers across the entire database."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(60*60*24))
    def get(self, request):
        # Top 10 Employers by total donation amount
        top_employers = Employer.objects.exclude(name='').order_by('-total_contributions')[:10]
        
        # Top 10 Individual Contributors by total donation amount
        top_contributors = Contributor.objects.exclude(full_name='UNKNOWN').order_by('-total_contributions')[:10]
        
        return Response({
            "top_employers": [{"name": e.name, "total": float(e.total_contributions)} for e in top_employers],
            "top_contributors": [{"name": c.full_name, "total": float(c.total_contributions)} for c in top_contributors]
        })

class ElectionListView(APIView):
    """Returns a list of unique elections (year, state, office) filtered by query params."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        state = request.query_params.get('state')
        office = request.query_params.get('office')
        
        # Get distinct combinations of year, state, office
        queryset = Candidate.objects.values(
            'CAND_ELECTION_YR', 
            'CAND_OFFICE_ST', 
            'CAND_OFFICE'
        ).distinct().order_by('-CAND_ELECTION_YR', 'CAND_OFFICE_ST', 'CAND_OFFICE')

        if state:
            queryset = queryset.filter(CAND_OFFICE_ST=state)
        if office:
            queryset = queryset.filter(CAND_OFFICE=office)

        results = [
            {
                "year": item['CAND_ELECTION_YR'],
                "state": item['CAND_OFFICE_ST'],
                "office": item['CAND_OFFICE']
            } for item in queryset
        ]
        
        return Response(results)