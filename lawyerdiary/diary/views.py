from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Case
from .forms import CaseForm
import openpyxl
from openpyxl.styles import Font, Alignment
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io

def case_list(request):
    cases = Case.objects.all().order_by('-hearing_date')
    filter_date = request.GET.get('hearing_date')
    if filter_date:
        cases = cases.filter(hearing_date=filter_date)
    context = {'cases': cases, 'filter_date': filter_date}
    return render(request, 'diary/case_list.html', context)

def case_add(request):
    if request.method == 'POST':
        form = CaseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('case_list')
    else:
        form = CaseForm()
    return render(request, 'diary/case_form.html', {'form': form})

def case_edit(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        form = CaseForm(request.POST, instance=case)
        if form.is_valid():
            form.save()
            return redirect('case_list')
    else:
        form = CaseForm(instance=case)
    return render(request, 'diary/case_form.html', {'form': form})

def case_delete(request, pk):
    case = get_object_or_404(Case, pk=pk)
    if request.method == 'POST':
        case.delete()
        return redirect('case_list')
    return render(request, 'diary/case_confirm_delete.html', {'case': case})

def download_excel(request):
    filter_date = request.GET.get('hearing_date')
    cases = Case.objects.all()
    if filter_date:
        cases = cases.filter(hearing_date=filter_date)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Cause List"

    headers = ['Case No', 'Manual Case No', 'Institution Date', 'Division', 'District', 'Tehsil',
               'Case Type', 'Act', 'Purpose', 'Section', 'Appellant', 'Respondent',
               'Hearing Date', 'Appellant Adv', 'Respondent Adv', 'Disposed']
    ws.append(headers)

    for col in range(1, len(headers)+1):
        cell = ws.cell(row=1, column=col)
        cell.font = Font(bold=True)
        cell.alignment = Alignment(horizontal='center')

    for case in cases:
        ws.append([
            case.case_no,
            case.manual_case_no or '',
            case.institution_date.strftime('%d-%m-%Y'),
            case.division_name,
            case.district_name,
            case.tehsil_name,
            case.case_type,
            case.act,
            case.case_purpose,
            case.section,
            case.appellant_name,
            case.respondent_name,
            case.hearing_date.strftime('%d-%m-%Y'),
            case.appellant_advocate,
            case.respondent_advocate,
            'Yes' if case.is_disposed else 'No'
        ])

    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[col_letter].width = adjusted_width

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename=cause_list_{filter_date or "all"}.xlsx'
    wb.save(response)
    return response

def download_pdf(request):
    filter_date = request.GET.get('hearing_date')
    cases = Case.objects.all()
    if filter_date:
        cases = cases.filter(hearing_date=filter_date)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Title
    p.setFont("Helvetica-Bold", 16)
    p.drawString(1*inch, height-1*inch, f"Cause List for {filter_date or 'All Dates'}")

    # Table headers
    p.setFont("Helvetica-Bold", 8)
    y = height - 1.5*inch
    x_offset = 0.5*inch
    headers = ['Case No', 'Appellant', 'Respondent', 'Hearing Date', 'Disposed']
    col_widths = [1.2*inch, 1.5*inch, 1.5*inch, 1*inch, 0.8*inch]

    for i, header in enumerate(headers):
        p.drawString(x_offset + sum(col_widths[:i]), y, header)

    # Data rows
    p.setFont("Helvetica", 8)
    y -= 0.2*inch
    for case in cases:
        if y < 1*inch:  # new page
            p.showPage()
            p.setFont("Helvetica", 8)
            y = height - 1*inch
            # Reprint headers on new page (optional)
            p.setFont("Helvetica-Bold", 8)
            for i, header in enumerate(headers):
                p.drawString(x_offset + sum(col_widths[:i]), y, header)
            p.setFont("Helvetica", 8)
            y -= 0.2*inch

        row = [
            case.case_no,
            case.appellant_name[:20],
            case.respondent_name[:20],
            case.hearing_date.strftime('%d-%m-%Y'),
            'Yes' if case.is_disposed else 'No'
        ]
        for i, value in enumerate(row):
            p.drawString(x_offset + sum(col_widths[:i]), y, str(value))
        y -= 0.2*inch

    p.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=cause_list_{filter_date or "all"}.pdf'
    return response
