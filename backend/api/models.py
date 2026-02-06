from django.db import models


class Office(models.Model):
    office_type = models.CharField(max_length=200)
    office_level = models.CharField(max_length=200)

class Party(models.Model):
    id = models.CharField(primary_key=True, max_length=1)
    name = models.CharField(max_length=200)

class Candidate(models.Model):
    CAND_ID = models.CharField("Candidate ID", max_length=9, primary_key=True)
    CAND_NAME = models.CharField("Candidate Name", max_length=200, null=True, blank=True)
    CAND_PTY_AFFILIATION = models.CharField("Party", max_length=3, null=True, blank=True)
    CAND_ELECTION_YR = models.IntegerField("Election Year", null=True, blank=True)
    CAND_OFFICE_ST = models.CharField("State", max_length=2, null=True, blank=True)
    CAND_OFFICE = models.CharField("Office", max_length=1, null=True, blank=True)
    CAND_OFFICE_DISTRICT = models.CharField("District", max_length=2, null=True, blank=True)
    CAND_ICI = models.CharField("Incumbent Status", max_length=1, null=True, blank=True)
    CAND_STATUS = models.CharField("Status", max_length=1, null=True, blank=True)
    CAND_PCC = models.CharField("Principal Committee", max_length=9, null=True, blank=True)
    CAND_ST1 = models.CharField("Street 1", max_length=34, null=True, blank=True)
    CAND_ST2 = models.CharField("Street 2", max_length=34, null=True, blank=True)
    CAND_CITY = models.CharField("City", max_length=30, null=True, blank=True)
    CAND_ST = models.CharField("Mailing State", max_length=2, null=True, blank=True)
    CAND_ZIP = models.CharField("ZIP", max_length=9, null=True, blank=True)

    class Meta:
        db_table = "api_candidate"

class Employer(models.Model):
    name = models.CharField(max_length=200)

class Contributor(models.Model):
    full_name = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=10)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

class Contribution(models.Model):
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    receipt_date = models.DateTimeField("receipt date")

class FECContribution(models.Model):
    CMTE_ID = models.CharField(
        "Filer identification number",
        max_length=9,
        help_text="9-character alpha-numeric code assigned to a committee by the FEC."
    )
    AMNDT_IND = models.CharField(
        "Amendment indicator",
        max_length=1,
        null=True, blank=True,
        help_text="N = New, A = Amendment, T = Termination."
    )
    RPT_TP = models.CharField(
        "Report type",
        max_length=3,
        null=True, blank=True,
        help_text="Type of report filed (e.g., 12G)."
    )
    TRANSACTION_PGI = models.CharField(
        "Primary-general indicator",
        max_length=5,
        null=True, blank=True,
        help_text="Election for which contribution was made (e.g., P2018)."
    )
    IMAGE_NUM = models.CharField(
        "Image number",
        max_length=18,
        null=True, blank=True,
        help_text="11- or 18-digit FEC image number."
    )
    TRANSACTION_TP = models.CharField(
        "Transaction type",
        max_length=4,
        null=True, blank=True,
        help_text="Transaction type code (e.g., 30T, 31E, etc.)."
    )
    ENTITY_TP = models.CharField(
        "Entity type",
        max_length=3,
        null=True, blank=True,
        help_text="CAN, CCM, COM, IND, ORG, PAC, PTY."
    )
    NAME = models.CharField(
        "Contributor name",
        max_length=200,
        null=True, blank=True
    )
    CITY = models.CharField(
        "City",
        max_length=30,
        null=True, blank=True
    )
    STATE = models.CharField(
        "State",
        max_length=2,
        null=True, blank=True
    )
    ZIP_CODE = models.CharField(
        "ZIP code",
        max_length=9,
        null=True, blank=True
    )
    EMPLOYER = models.CharField(
        "Employer",
        max_length=38,
        null=True, blank=True
    )
    OCCUPATION = models.CharField(
        "Occupation",
        max_length=38,
        null=True, blank=True
    )
    TRANSACTION_DT = models.DateField(
        "Transaction date",
        null=True, blank=True
    )
    TRANSACTION_AMT = models.DecimalField(
        "Transaction amount",
        max_digits=14,
        decimal_places=2,
        null=True, blank=True
    )
    OTHER_ID = models.CharField(
        "Other ID",
        max_length=9,
        null=True, blank=True,
        help_text="Contributor’s FEC ID (if committee or candidate)."
    )
    TRAN_ID = models.CharField(
        "Transaction ID",
        max_length=32,
        null=True, blank=True,
        help_text="Unique ID for each transaction in a report."
    )
    FILE_NUM = models.BigIntegerField(
        "File number / Report ID",
        null=True, blank=True
    )
    MEMO_CD = models.CharField(
        "Memo code",
        max_length=1,
        null=True, blank=True,
        help_text="'X' indicates memo item (not part of total)."
    )
    MEMO_TEXT = models.CharField(
        "Memo text",
        max_length=100,
        null=True, blank=True
    )
    SUB_ID = models.BigIntegerField(
        "FEC record number",
        primary_key=True, unique=True,
        help_text="Unique row ID (required)."
    )

    class Meta:
        verbose_name = "FEC Contribution"
        verbose_name_plural = "FEC Contributions"
        ordering = ["-TRANSACTION_DT"]
        indexes = [
            models.Index(fields=["CMTE_ID"]),
            models.Index(fields=["NAME"]),
            models.Index(fields=["TRANSACTION_DT"]),
            models.Index(fields=["TRANSACTION_AMT"]),
        ]

    def __str__(self):
        return f"{self.NAME or 'Unknown'} ({self.CMTE_ID}) - ${self.TRANSACTION_AMT or 0}"


class Committee(models.Model):
    CMTE_ID = models.CharField(
        "Committee ID",
        max_length=9,
        unique=True,
        primary_key=True,  # This replaces the automatic 'id' column
        help_text="9-character ID assigned by the FEC."
    )
    CMTE_NM = models.CharField(
        "Committee Name",
        max_length=200,
        blank=True,
        null=True
    )
    TRES_NM = models.CharField(
        "Treasurer's Name",
        max_length=90,
        blank=True,
        null=True,
        help_text="Officially registered treasurer for the committee."
    )
    CMTE_ST1 = models.CharField(
        "Street 1",
        max_length=34,
        blank=True,
        null=True
    )
    CMTE_ST2 = models.CharField(
        "Street 2",
        max_length=34,
        blank=True,
        null=True
    )
    CMTE_CITY = models.CharField(
        "City",
        max_length=30,
        blank=True,
        null=True
    )
    CMTE_ST = models.CharField(
        "State",
        max_length=2,
        blank=True,
        null=True
    )
    CMTE_ZIP = models.CharField(
        "ZIP Code",
        max_length=9,
        blank=True,
        null=True
    )
    CMTE_DSGN = models.CharField(
        "Committee Designation",
        max_length=1,
        blank=True,
        null=True,
        help_text="A=Authorized, B=Lobbyist, D=Leadership, J=Joint, P=Principal, U=Unauthorized"
    )
    CMTE_TP = models.CharField(
        "Committee Type",
        max_length=1,
        blank=True,
        null=True,
        help_text="Single-character committee type code."
    )
    CMTE_PTY_AFFILIATION = models.CharField(
        "Party Affiliation",
        max_length=3,
        blank=True,
        null=True
    )
    CMTE_FILING_FREQ = models.CharField(
        "Filing Frequency",
        max_length=1,
        blank=True,
        null=True,
        help_text="A=Admin terminated, D=Debt, M=Monthly, Q=Quarterly, T=Terminated, W=Waived"
    )
    ORG_TP = models.CharField(
        "Interest Group Category",
        max_length=1,
        blank=True,
        null=True,
        help_text="C=Corporation, L=Labor, M=Membership, T=Trade, V=Cooperative, W=Corp w/o capital stock"
    )
    CONNECTED_ORG_NM = models.CharField(
        "Connected Organization Name",
        max_length=200,
        blank=True,
        null=True
    )
    CAND_ID = models.CharField(
        "Candidate ID",
        max_length=9,
        blank=True,
        null=True,
        help_text="Candidate ID (if applicable)"
    )

    class Meta:
        db_table = "api_committee"
        verbose_name = "FEC Committee"
        verbose_name_plural = "FEC Committees"

    def __str__(self):
        return f"{self.CMTE_NM or self.CMTE_ID}"