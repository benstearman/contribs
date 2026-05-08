from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Q
from django.db import connection
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
import re
from .models import Contributor, Contribution, Candidate, Committee, Party, Employer
from rest_framework.views import APIView
from .serializers import (
    ContributionSerializer, 
    ContributorSerializer, 
    CandidateSerializer, 
    CommitteeSerializer, 
    PartySerializer
)

# --- Optimized Pagination ---

class FastPaginator(Paginator):
    """
    Uses PostgreSQL EXPLAIN to get a fast row count estimate for large tables.
    Standard COUNT(*) is too slow on millions of records.
    """
    @property
    def count(self):
        if not hasattr(self, '_count') or self._count is None:
            try:
                if hasattr(self.object_list, 'query'):
                    with connection.cursor() as cursor:
                        sql, params = self.object_list.query.sql_with_params()
                        cursor.execute(f"EXPLAIN {sql}", params)
                        result = cursor.fetchone()[0]
                        # Extract row estimate from EXPLAIN output (e.g. "rows=1234567")
                        match = re.search(r'rows=(\d+)', result)
                        if match:
                            self._count = int(match.group(1))
                        else:
                            self._count = super().count
                else:
                    self._count = super().count
            except Exception:
                self._count = super().count
        return self._count

class FastCountPagination(PageNumberPagination):
    django_paginator_class = FastPaginator
    page_size = 10

# --- Optimized Search & Filter Backends ---

class OptimizedContributionSearchFilter(filters.BaseFilterBackend):
    """
    Optimized search for the multi-million row Contribution table.
    Leverages Trigram GIN indexes on related tables to avoid slow multi-table joins.
    """
    search_param = 'search'

    def filter_queryset(self, request, queryset, view):
        search_query = request.query_params.get(self.search_param)
        if not search_query or len(search_query) < 2:
            return queryset
            
        # Use subqueries to keep filtering logic inside the database
        contributor_subquery = Contributor.objects.filter(full_name__icontains=search_query).values('id')
        candidate_subquery = Candidate.objects.filter(CAND_NAME__icontains=search_query).values('CAND_ID')
        committee_subquery = Committee.objects.filter(
            Q(CMTE_NM__icontains=search_query) | Q(CAND_ID__in=candidate_subquery)
        ).values('CMTE_ID')
        
        return queryset.filter(
            Q(contributor__in=contributor_subquery) | Q(committee__in=committee_subquery)
        )

class ContributionAmountFilter(filters.BaseFilterBackend):
    """Filters contributions by a dollar amount range."""
    def filter_queryset(self, request, queryset, view):
        min_amount = request.query_params.get('min_amount')
        max_amount = request.query_params.get('max_amount')
        if min_amount:
            queryset = queryset.filter(amount__gte=min_amount)
        if max_amount:
            queryset = queryset.filter(amount__lte=max_amount)
        return queryset

class CandidateFilterBackend(filters.BaseFilterBackend):
    """Handles state, office, and year filtering for candidates."""
    def filter_queryset(self, request, queryset, view):
        state = request.query_params.get('state')
        office = request.query_params.get('office')
        year = request.query_params.get('year')
        
        if state:
            queryset = queryset.filter(CAND_OFFICE_ST=state)
        if office:
            queryset = queryset.filter(CAND_OFFICE=office)
        if year:
            queryset = queryset.filter(CAND_ELECTION_YR=year)
            
        return queryset

# --- ViewSets ---

class PartyViewSet(viewsets.ReadOnlyModelViewSet):
    """View political party codes and names."""
    queryset = Party.objects.all().order_by('id')
    serializer_class = PartySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class CandidateViewSet(viewsets.ModelViewSet):
    """View and edit candidate details with Trigram search and custom filters."""
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = FastCountPagination
    filter_backends = [filters.SearchFilter, CandidateFilterBackend]
    search_fields = ['CAND_NAME']

    def get_queryset(self):
        return Candidate.objects.select_related('CAND_PTY_AFFILIATION').all().order_by("-total_contributions", "CAND_NAME")

    @action(detail=True, methods=['get'])
    def committees(self, request, pk=None):
        candidate = self.get_object()
        committees = candidate.committees.all()
        serializer = CommitteeSerializer(committees, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def top_contributors(self, request, pk=None):
        candidate = self.get_object()
        committees = candidate.committees.all()
        
        top_individuals = Contribution.objects.filter(committee__in=committees) \
            .values('contributor__full_name', 'contributor__employer__name') \
            .annotate(total=Sum('amount')) \
            .order_by('-total')[:10]
        
        top_employers = Contribution.objects.filter(committee__in=committees) \
            .values('contributor__employer__name') \
            .exclude(contributor__employer__name__isnull=True) \
            .exclude(contributor__employer__name='') \
            .annotate(total=Sum('amount')) \
            .order_by('-total')[:10]
            
        return Response({
            "top_individuals": [
                {
                    "name": item['contributor__full_name'], 
                    "total": float(item['total'] or 0.0),
                    "employer_name": item['contributor__employer__name']
                } for item in top_individuals
            ],
            "top_employers": [
                {
                    "name": item['contributor__employer__name'], 
                    "total": float(item['total'] or 0.0)
                } for item in top_employers
            ]
        })
    
class CommitteeViewSet(viewsets.ModelViewSet):
    """View and edit committee details."""
    queryset = Committee.objects.select_related('CAND_ID').all().order_by("CMTE_NM")
    serializer_class = CommitteeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = FastCountPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['CMTE_NM']

class ContributionViewSet(viewsets.ModelViewSet):
    """View and edit individual contributions with high-performance search."""
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = FastCountPagination
    # Combined search and amount filtering
    filter_backends = [OptimizedContributionSearchFilter, ContributionAmountFilter]

    def get_queryset(self):
        return Contribution.objects.select_related(
            'contributor', 
            'committee', 
            'committee__CAND_ID'
        ).all().order_by("-receipt_date")

class ContributorViewSet(viewsets.ModelViewSet):
    """View and edit contributor profiles."""
    queryset = Contributor.objects.select_related('employer').all().order_by("full_name")
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = FastCountPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name']

# --- Summary Views ---

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class ElectionSummaryView(APIView):
    """Calculates top contributors and employers across the entire database."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(60*60*24))
    def get(self, request):
        top_employers = Employer.objects.exclude(name='').order_by('-total_contributions')[:10]
        top_contributors = Contributor.objects.exclude(full_name='UNKNOWN').order_by('-total_contributions')[:10]
        
        return Response({
            "top_employers": [{"name": e.name, "total": float(e.total_contributions)} for e in top_employers],
            "top_contributors": [{"name": c.full_name, "total": float(c.total_contributions)} for c in top_contributors]
        })

class ElectionListView(APIView):
    """Returns a list of unique elections (year, state, office) with total contributions."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        state = request.query_params.get('state')
        office = request.query_params.get('office')
        
        queryset = Candidate.objects.values(
            'CAND_ELECTION_YR', 
            'CAND_OFFICE_ST', 
            'CAND_OFFICE'
        ).annotate(
            total_amount=Sum('total_contributions')
        ).order_by('-total_amount')

        if state:
            queryset = queryset.filter(CAND_OFFICE_ST=state)
        if office:
            queryset = queryset.filter(CAND_OFFICE=office)

        results = [
            {
                "year": item['CAND_ELECTION_YR'],
                "state": item['CAND_OFFICE_ST'],
                "office": item['CAND_OFFICE'],
                "total_amount": float(item['total_amount'] or 0.0)
            } for item in queryset
        ]
        
        return Response(results)

class CandidateFiltersView(APIView):
    """Returns unique states and offices available in the database."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        states = Candidate.objects.exclude(CAND_OFFICE_ST__isnull=True).exclude(CAND_OFFICE_ST='').values_list('CAND_OFFICE_ST', flat=True).distinct().order_by('CAND_OFFICE_ST')
        
        offices = [
            {"id": "H", "name": "House"},
            {"id": "S", "name": "Senate"},
            {"id": "P", "name": "President"}
        ]
        
        return Response({
            "states": list(states),
            "offices": offices
        })
