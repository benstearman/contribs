from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db import models, connection
from django.db.models import Sum, Q
from django.utils.functional import cached_property
from django.core.paginator import Paginator
from .models import Contributor, Contribution, Candidate, Committee, Party, Employer
from rest_framework.views import APIView

import re

class FastCountPaginator(Paginator):
    @cached_property
    def count(self):
        """
        Optimized count for PostgreSQL using EXPLAIN to avoid slow COUNT(*).
        """
        if connection.vendor == 'postgresql':
            try:
                # Use EXPLAIN to get an estimated count from the query planner
                with connection.cursor() as cursor:
                    sql, params = self.object_list.query.sql_with_params()
                    cursor.execute(f"EXPLAIN {sql}", params)
                    explain_output = cursor.fetchone()[0]
                    # The output usually contains 'rows=N'
                    match = re.search(r'rows=(\d+)', explain_output)
                    if match:
                        count = int(match.group(1))
                        # Only return estimate if it's significantly large
                        if count > 1000:
                            return count
            except Exception:
                # Fallback to a safe large number if explain fails
                return 1000000
        
        # Fallback to standard count for small tables or non-Postgres
        return super().count

class FastCountPagination(PageNumberPagination):
    django_paginator_class = FastCountPaginator
    page_size = 10
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
    pagination_class = FastCountPagination

    filter_backends = [filters.SearchFilter]
    search_fields = ['CAND_NAME']

    def get_queryset(self):
        queryset = Candidate.objects.select_related('CAND_PTY_AFFILIATION').all().order_by("-total_contributions", "CAND_NAME")
        
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

    @action(detail=True, methods=['get'])
    def top_contributors(self, request, pk=None):
        candidate = self.get_object()
        committees = candidate.committees.all()
        
        # Aggregate top individuals
        top_individuals = Contribution.objects.filter(committee__in=committees) \
            .values('contributor__full_name', 'contributor__employer__name') \
            .annotate(total=Sum('amount')) \
            .order_by('-total')[:10]
        
        # Aggregate top employers
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
    # select_related avoids extra queries for the supported candidate
    queryset = Committee.objects.select_related('CAND_ID').all().order_by("CMTE_NM")
    serializer_class = CommitteeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = FastCountPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['CMTE_NM']

class ContributionViewSet(viewsets.ModelViewSet):
    """View and edit individual contributions."""
    serializer_class = ContributionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = FastCountPagination

    # Optimized base queryset for joins
    queryset = Contribution.objects.select_related(
        'contributor', 
        'committee', 
        'committee__CAND_ID'
    ).all()

    def get_queryset(self):
        # Always start with a fresh queryset clone
        queryset = Contribution.objects.select_related(
            'contributor', 
            'committee', 
            'committee__CAND_ID'
        ).all()
        
        search = self.request.query_params.get('search')
        if search:
            # Direct Index Filtering: Search parent tables first to maximize GIN index efficiency.
            # Trigram indexes (gin_trgm_ops) make these lookups extremely fast even with millions of rows.
            contributor_ids = Contributor.objects.filter(full_name__icontains=search).values_list('id', flat=True)[:1000]
            committee_ids = Committee.objects.filter(CMTE_NM__icontains=search).values_list('CMTE_ID', flat=True)[:1000]
            candidate_ids = Candidate.objects.filter(CAND_NAME__icontains=search).values_list('CAND_ID', flat=True)[:1000]

            queryset = queryset.filter(
                Q(contributor_id__in=contributor_ids) |
                Q(committee_id__in=committee_ids) |
                Q(committee__CAND_ID_id__in=candidate_ids)
            )
            
        return queryset.order_by("-receipt_date")

class ContributorViewSet(viewsets.ModelViewSet):
    """View and edit contributor profiles."""
    queryset = Contributor.objects.select_related('employer').all().order_by("full_name")
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = FastCountPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['full_name']

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
    """Returns a list of unique elections (year, state, office) filtered by query params, with total contributions."""
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        state = request.query_params.get('state')
        office = request.query_params.get('office')
        
        # Group by year, state, office and sum candidate totals
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
        
        # Hardcoded based on model choices
        offices = [
            {"id": "H", "name": "House"},
            {"id": "S", "name": "Senate"},
            {"id": "P", "name": "President"}
        ]
        
        return Response({
            "states": list(states),
            "offices": offices
        })