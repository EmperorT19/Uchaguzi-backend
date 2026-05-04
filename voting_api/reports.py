import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.utils import timezone
from .models import Vote, Voter, Candidate, Seat
from django.db.models import Count

def _generate_pdf_response(filename):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
    return response

def get_base_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='CenterTitle', parent=styles['Heading1'], alignment=1, spaceAfter=20))
    return styles

def admin_report_election_results(request):
    response = _generate_pdf_response('Election_Results_Summary')
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = get_base_styles()
    
    elements.append(Paragraph("Election Results Summary", styles['CenterTitle']))
    elements.append(Paragraph(f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    seats = Seat.objects.all()
    data = [['Seat', 'Leading Candidate', 'Party', 'Votes']]
    
    for seat in seats:
        top_cand = Vote.objects.filter(seat=seat).values('candidate__full_name', 'candidate__party').annotate(votes=Count('id')).order_by('-votes').first()
        if top_cand:
            data.append([
                seat.name,
                top_cand['candidate__full_name'],
                top_cand['candidate__party'],
                str(top_cand['votes'])
            ])
            
    if len(data) > 1:
        t = Table(data, colWidths=[150, 150, 100, 80])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ]))
        elements.append(t)
    else:
        elements.append(Paragraph("No votes recorded yet.", styles['Normal']))
        
    doc.build(elements)
    return response

def admin_report_voter_turnout(request):
    response = _generate_pdf_response('Voter_Turnout_Report')
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = get_base_styles()
    
    elements.append(Paragraph("Voter Turnout Report", styles['CenterTitle']))
    elements.append(Paragraph(f"Generated: {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    elements.append(Spacer(1, 20))

    total_voters = Voter.objects.count()
    active_voters = Vote.objects.values('voter').distinct().count()
    total_votes = Vote.objects.count()
    turnout_pct = (active_voters / total_voters * 100) if total_voters > 0 else 0

    data = [
        ['Metric', 'Value'],
        ['Total Registered Voters', str(total_voters)],
        ['Voters Who Cast Ballots', str(active_voters)],
        ['Total Votes Cast', str(total_votes)],
        ['Overall Turnout %', f"{turnout_pct:.1f}%"],
    ]
    
    t = Table(data, colWidths=[250, 150])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.darkblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 12),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    elements.append(t)
        
    doc.build(elements)
    return response

def admin_report_registered_voters(request):
    response = _generate_pdf_response('Registered_Voters_List')
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = get_base_styles()
    
    elements.append(Paragraph("Registered Voters List", styles['CenterTitle']))
    elements.append(Paragraph("Confidential Internal Document - Passwords Excluded", styles['Normal']))
    elements.append(Spacer(1, 20))

    voters = Voter.objects.all().order_by('-created_at')
    data = [['Voter Code', 'Full Name', 'County', 'Constituency', 'Registered At']]
    
    for v in voters:
        data.append([
            v.voter_code,
            v.full_name,
            str(v.county) if v.county else "N/A",
            str(v.constituency) if v.constituency else "N/A",
            v.created_at.strftime('%Y-%m-%d %H:%M')
        ])
            
    if len(data) > 1:
        t = Table(data, colWidths=[80, 150, 80, 80, 100])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkgreen),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
        ]))
        elements.append(t)
    else:
        elements.append(Paragraph("No voters registered.", styles['Normal']))
        
    doc.build(elements)
    return response

def admin_report_audit_trail(request):
    response = _generate_pdf_response('Audit_Trail_Log')
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = get_base_styles()
    
    elements.append(Paragraph("Live Audit Trail Log", styles['CenterTitle']))
    elements.append(Spacer(1, 20))

    votes = Vote.objects.select_related('voter', 'seat', 'candidate').order_by('-voted_at')
    data = [['Timestamp', 'Voter Code', 'Seat', 'Candidate Selected']]
    
    for v in votes:
        data.append([
            v.voted_at.strftime('%Y-%m-%d %H:%M:%S'),
            v.voter.voter_code,
            v.seat.name[:30] + "..." if len(v.seat.name)>30 else v.seat.name,
            v.candidate.full_name
        ])
            
    if len(data) > 1:
        t = Table(data, colWidths=[110, 80, 160, 130])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.darkred),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
        ]))
        elements.append(t)
    else:
        elements.append(Paragraph("No votes cast.", styles['Normal']))
        
    doc.build(elements)
    return response

def admin_report_candidate_performance(request):
    response = _generate_pdf_response('Candidate_Performance_Report')
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = get_base_styles()
    
    elements.append(Paragraph("Candidate Performance Report", styles['CenterTitle']))
    elements.append(Spacer(1, 20))

    candidates = Vote.objects.values('candidate__full_name', 'candidate__party', 'seat__name').annotate(votes=Count('id')).order_by('-votes')[:500]
    data = [['Candidate', 'Party', 'Seat', 'Total Votes']]
    
    for c in candidates:
        data.append([
            c['candidate__full_name'],
            c['candidate__party'],
            c['seat__name'][:30] + "..." if len(c['seat__name'])>30 else c['seat__name'],
            str(c['votes'])
        ])
            
    if len(data) > 1:
        t = Table(data, colWidths=[150, 100, 160, 70])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.black),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey)
        ]))
        elements.append(t)
    else:
        elements.append(Paragraph("No candidates have received votes.", styles['Normal']))
        
    doc.build(elements)
    return response
