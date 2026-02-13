from rest_framework import serializers
from .models import Party, Candidate, Committee, Employer, Contributor, Contribution

class PartySerializer(serializers.ModelSerializer):
    """Returns basic party info (e.g., Republican, Democratic)."""
    class Meta:
        model = Party
        fields = ["id", "name"]

class CandidateSerializer(serializers.ModelSerializer):
    """Provides details about the candidate, including their party affiliation."""
    party_name = serializers.CharField(source="CAND_PTY_AFFILIATION.name", read_only=True)
    office_display = serializers.CharField(source="get_CAND_OFFICE_display", read_only=True)

    class Meta:
        model = Candidate
        fields = ["CAND_ID", "CAND_NAME", "party_name", "CAND_ELECTION_YR", "office_display", "CAND_OFFICE_ST"]

class CommitteeSerializer(serializers.ModelSerializer):
    """Details the committee and the candidate they support."""
    candidate_name = serializers.CharField(source="CAND_ID.CAND_NAME", read_only=True)

    class Meta:
        model = Committee
        fields = ["CMTE_ID", "CMTE_NM", "CMTE_TP", "candidate_name"]

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