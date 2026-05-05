from rest_framework import serializers
from .models import Party, Candidate, Committee, Employer, Contributor, Contribution

import datetime
import json
import os
from django.conf import settings

def load_legislator_data():
    try:
        file_path = os.path.join(settings.BASE_DIR, 'legislators-current.json')
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        fec_map = {}
        for leg in data:
            bioguide = leg.get('id', {}).get('bioguide')
            fec_ids = leg.get('id', {}).get('fec', [])
            if bioguide and fec_ids:
                for fec in fec_ids:
                    fec_map[fec] = bioguide
        return fec_map
    except (FileNotFoundError, AttributeError):
        print("WARNING: legislators-current.json not found. Photos won't load.")
        return {}

FEC_TO_BIOGUIDE = load_legislator_data()

class SmartDateField(serializers.DateField):
    """
    Custom DateField that safely handles datetime objects by converting 
    them to dates before representation.
    """
    def to_representation(self, value):
        if isinstance(value, datetime.datetime):
            value = value.date()
        return super().to_representation(value)

class PartySerializer(serializers.ModelSerializer):
    """Returns basic party info (e.g., Republican, Democratic)."""
    class Meta:
        model = Party
        fields = ["id", "name"]

class CandidateSerializer(serializers.ModelSerializer):
    """Provides details about the candidate, including their party affiliation."""
    party_name = serializers.CharField(source="CAND_PTY_AFFILIATION.name", read_only=True)
    office_display = serializers.CharField(source="get_CAND_OFFICE_display", read_only=True)
    total_contributions = serializers.DecimalField(max_digits=14, decimal_places=2, read_only=True)

    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = Candidate
        fields = [
            "CAND_ID",
            "CAND_NAME",
            "party_name",
            "CAND_ELECTION_YR",
            "office_display",
            "CAND_OFFICE_ST",
            "total_contributions",
            "photo_url"
        ]

    def get_photo_url(self, obj):
        bioguide_id = FEC_TO_BIOGUIDE.get(obj.CAND_ID)
        if bioguide_id:
            return f"https://unitedstates.github.io/images/congress/225x275/{bioguide_id}.jpg"
        return None

class CommitteeSerializer(serializers.ModelSerializer):
    """Details the committee and the candidate they support."""
    candidate_name = serializers.CharField(source="CAND_ID.CAND_NAME", read_only=True)

    total_contributions = serializers.FloatField(read_only=True)

    class Meta:
        model = Committee
        fields = ["CMTE_ID", "CMTE_NM", "CMTE_TP", "candidate_name", "CAND_ID", "TRES_NM", "total_contributions"]
        
class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employer
        fields = ["name"]

class ContributorSerializer(serializers.ModelSerializer):
    """Detailed contributor info with nested employer data."""
    employer_name = serializers.CharField(source="employer.name", read_only=True)

    class Meta:
        model = Contributor
        fields = ["id", "full_name", "zip_code", "employer_name"]

class ContributionSerializer(serializers.ModelSerializer):
    """
    The main serializer for contributions. 
    Includes primary keys for editing but can provide nested detail for viewing.
    """
    # Use nested serializers for more detailed GET responses
    contributor_detail = ContributorSerializer(source="contributor", read_only=True)
    committee_detail = CommitteeSerializer(source="committee", read_only=True)
    receipt_date = SmartDateField()

    class Meta:
        model = Contribution
        fields = [
            "id", 
            "amount", 
            "receipt_date", 
            "contributor",    # PrimaryKey field for writes
            "committee",      # PrimaryKey field for writes
            "contributor_detail", 
            "committee_detail",
            "fec_sub_id"
        ]
