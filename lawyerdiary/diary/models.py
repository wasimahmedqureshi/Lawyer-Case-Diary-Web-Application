from django.db import models

class Case(models.Model):
    case_no = models.CharField(max_length=50, unique=True, verbose_name="Case Number")
    manual_case_no = models.CharField(max_length=50, blank=True, null=True, verbose_name="Manual Case No")
    institution_date = models.DateField(verbose_name="Institution Date")
    division_name = models.CharField(max_length=100, verbose_name="Division Name")
    district_name = models.CharField(max_length=100, verbose_name="District Name")
    tehsil_name = models.CharField(max_length=100, verbose_name="Tehsil Name")
    case_type = models.CharField(max_length=100, verbose_name="Case Type")
    act = models.CharField(max_length=200, verbose_name="Act")
    case_purpose = models.TextField(verbose_name="Case Purpose")
    section = models.CharField(max_length=100, verbose_name="Section")
    appellant_name = models.CharField(max_length=200, verbose_name="Appellant Name")
    respondent_name = models.CharField(max_length=200, verbose_name="Respondent Name")
    hearing_date = models.DateField(verbose_name="Next Hearing Date")
    appellant_advocate = models.CharField(max_length=200, verbose_name="Appellant Advocate")
    respondent_advocate = models.CharField(max_length=200, verbose_name="Respondent Advocate")
    is_disposed = models.BooleanField(default=False, verbose_name="Disposed")
    disposal_date = models.DateField(blank=True, null=True, verbose_name="Disposal Date")

    def __str__(self):
        return f"{self.case_no} - {self.appellant_name} vs {self.respondent_name}"
