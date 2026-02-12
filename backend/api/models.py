from django.db import models

class Party(models.Model):
    id = models.CharField(primary_key=True, max_length=3) # FEC uses 3-letter codes
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Party"
        verbose_name_plural = "Parties"

    def __str__(self):
        return f"{self.name} ({self.id})"

class Candidate(models.Model):
    CAND_ID = models.CharField("Candidate ID", max_length=9, primary_key=True)
    CAND_NAME = models.CharField("Candidate Name", max_length=200, db_index=True)
    CAND_PTY_AFFILIATION = models.ForeignKey(Party, on_delete=models.SET_NULL, null=True, blank=True)
    CAND_ELECTION_YR = models.IntegerField("Election Year", db_index=True)
    CAND_OFFICE_ST = models.CharField("State", max_length=2, null=True, blank=True)
    CAND_OFFICE = models.CharField("Office", max_length=1, choices=[('H', 'House'), ('S', 'Senate'), ('P', 'President')])
    CAND_OFFICE_DISTRICT = models.CharField("District", max_length=2, null=True, blank=True)
    
    class Meta:
        db_table = "api_candidate"
        indexes = [models.Index(fields=['CAND_NAME', 'CAND_ELECTION_YR'])]

    def __str__(self):
        return f"{self.CAND_NAME} ({self.CAND_ID})"

class Committee(models.Model):
    CMTE_ID = models.CharField("Committee ID", max_length=9, primary_key=True)
    CMTE_NM = models.CharField("Committee Name", max_length=200, db_index=True)
    TRES_NM = models.CharField("Treasurer Name", max_length=90, null=True, blank=True)
    CMTE_ST = models.CharField("State", max_length=2, null=True, blank=True)
    CMTE_TP = models.CharField("Committee Type", max_length=1, null=True, blank=True)
    CMTE_DSGN = models.CharField("Designation", max_length=1, null=True, blank=True)
    CAND_ID = models.ForeignKey(Candidate, on_delete=models.SET_NULL, null=True, blank=True, related_name='committees')

    class Meta:
        db_table = "api_committee"

    def __str__(self):
        return self.CMTE_NM or self.CMTE_ID

class Employer(models.Model):
    name = models.CharField(max_length=200, unique=True, db_index=True)

    def __str__(self):
        return self.name

class Contributor(models.Model):
    full_name = models.CharField(max_length=200, db_index=True)
    zip_code = models.CharField(max_length=10, db_index=True)
    employer = models.ForeignKey(Employer, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        # Prevents duplicate contributors during import
        unique_together = ('full_name', 'zip_code')

    def __str__(self):
        return self.full_name

class Contribution(models.Model):
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE, related_name='contributions')
    committee = models.ForeignKey(Committee, on_delete=models.CASCADE, related_name='contributions')
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    receipt_date = models.DateField(db_index=True)
    fec_sub_id = models.BigIntegerField(unique=True, null=True, help_text="Original FEC SUB_ID")

    class Meta:
        ordering = ['-receipt_date']

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