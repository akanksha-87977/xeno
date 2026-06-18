from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from typing import List
from datetime import datetime
import pandas as pd
from ..schemas.validation import ValidationError

class ReportGeneratorService:
    
    @staticmethod
    def generate_error_report_csv(errors: List[ValidationError], filename: str) -> str:
        """Generate CSV error report"""
        if not errors:
            return None
        
        df = pd.DataFrame([
            {
                "Row Number": error.row_number,
                "Column Name": error.column_name,
                "Error Type": error.error_type,
                "Error Description": error.error_description,
                "Current Value": error.current_value or "",
                "Suggested Fix": error.suggested_fix or ""
            }
            for error in errors
        ])
        
        df.to_csv(filename, index=False)
        return filename
    
    @staticmethod
    def generate_error_report_excel(errors: List[ValidationError], filename: str) -> str:
        """Generate Excel error report"""
        if not errors:
            return None
        
        df = pd.DataFrame([
            {
                "Row Number": error.row_number,
                "Column Name": error.column_name,
                "Error Type": error.error_type,
                "Error Description": error.error_description,
                "Current Value": error.current_value or "",
                "Suggested Fix": error.suggested_fix or ""
            }
            for error in errors
        ])
        
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Errors', index=False)
            
            # Auto-adjust column widths
            worksheet = writer.sheets['Errors']
            for idx, col in enumerate(df.columns):
                max_length = max(df[col].astype(str).apply(len).max(), len(col)) + 2
                worksheet.column_dimensions[chr(65 + idx)].width = min(max_length, 50)
        
        return filename
    
    @staticmethod
    def generate_error_report_pdf(
        errors: List[ValidationError],
        filename: str,
        summary: dict
    ) -> str:
        """Generate PDF error report"""
        doc = SimpleDocTemplate(filename, pagesize=A4)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=30,
            alignment=1  # Center
        )
        
        title = Paragraph("Validation Error Report", title_style)
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # Summary section
        summary_data = [
            ['Metric', 'Value'],
            ['Report Generated', datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
            ['Total Records', f"{summary.get('total_records', 0):,}"],
            ['Valid Records', f"{summary.get('valid_records', 0):,}"],
            ['Invalid Records', f"{summary.get('invalid_records', 0):,}"],
            ['Success Rate', f"{summary.get('success_rate', 0):.2f}%"],
            ['Total Errors', f"{len(errors):,}"]
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # Errors section
        if errors:
            errors_title = Paragraph("Detailed Errors", styles['Heading2'])
            elements.append(errors_title)
            elements.append(Spacer(1, 0.2*inch))
            
            # Show first 100 errors
            error_data = [['Row', 'Column', 'Error Type', 'Description']]
            for error in errors[:100]:
                error_data.append([
                    str(error.row_number),
                    error.column_name,
                    error.error_type.replace('_', ' '),
                    error.error_description[:50] + '...' if len(error.error_description) > 50 else error.error_description
                ])
            
            error_table = Table(error_data, colWidths=[0.7*inch, 1.5*inch, 1.5*inch, 3*inch])
            error_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4472C4')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            
            elements.append(error_table)
            
            if len(errors) > 100:
                note = Paragraph(
                    f"<i>Note: Showing first 100 errors out of {len(errors)} total errors.</i>",
                    styles['Normal']
                )
                elements.append(Spacer(1, 0.2*inch))
                elements.append(note)
        
        doc.build(elements)
        return filename