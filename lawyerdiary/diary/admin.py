from django.contrib import admin
from .models import Case

@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('case_no', 'appellant_name', 'respondent_name', 'hearing_date', 'is_disposed')
    list_filter = ('is_disposed', 'division_name')
    search_fields = ('case_no', 'appellant_name', 'respondent_name')
