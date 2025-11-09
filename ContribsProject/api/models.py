from django.db import models


class Office(models.Model):
    office_type = models.CharField(max_length=200)
    office_level = models.CharField(max_length=200)

class Party(models.Model):
    id = models.CharField(primary_key=True, max_length=1)
    name = models.CharField(max_length=200)

class Candidate(models.Model):
    office = models.ForeignKey(Office, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    party = models.ForeignKey(Party, on_delete=models.CASCADE)

class Employer(models.Model):
    name = models.CharField(max_length=200)

class Contributor(models.Model):
    full_name = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=10)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

class Contribution(models.Model):
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    receipt_date = models.DateTimeField("receipt date")
