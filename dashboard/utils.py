from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime
from django.utils import timezone


def generate_product_pdf(products, title="Product Report"):
    """
    Generate PDF for products (single or multiple)
    
    Args:
        products: QuerySet of Product objects
        title: Title for the PDF document
    
    Returns:
        BytesIO buffer containing PDF data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,  # Center alignment
        textColor=colors.darkblue
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=20,
        alignment=1,
        textColor=colors.grey
    )
    
    story = []
    
    # Title
    story.append(Paragraph(title, title_style))
    
    # Generated timestamp
    current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"Generated on: {current_time}", subtitle_style))
    story.append(Spacer(1, 20))
    
    # Products data
    data = []
    
    # Table headers
    headers = ['ID', 'Name', 'Category', 'Price', 'Status', 'Stock', 'Created Date']
    data.append(headers)
    
    # Product data
    for product in products:
        row = [
            str(product.id),
            product.name[:30] + '...' if len(product.name) > 30 else product.name,
            product.category.name if product.category else 'N/A',
            f"Rs. {product.price:.2f}",
            product.get_status_display(),
            str(product.stock_quantity) if hasattr(product, 'stock_quantity') else 'N/A',
            product.created_at.strftime("%Y-%m-%d") if product.created_at else 'N/A'
        ]
        data.append(row)
    
    # Create table
    table = Table(data, colWidths=[0.5*inch, 2*inch, 1.2*inch, 0.8*inch, 1*inch, 0.8*inch, 1*inch])
    
    # Style the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F9FAFB')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    
    table.setStyle(style)
    
    # Alternate row colors
    row_count = len(data)
    for i in range(1, row_count):
        if i % 2 == 0:
            bc = colors.HexColor('#FFFFFF')
        else:
            bc = colors.HexColor('#F9FAFB')
        ts = TableStyle([('BACKGROUND', (0, i), (-1, i), bc)])
        table.setStyle(ts)
    
    story.append(table)
    
    # Add summary if multiple products
    if products.count() > 1:
        story.append(Spacer(1, 20))
        
        total_products = products.count()
        total_value = sum(p.price for p in products)
        in_stock = products.filter(status='in_stock').count()
        out_of_stock = products.filter(status='out_of_stock').count()
        
        summary_data = [
            ['Summary Statistics', ''],
            ['Total Products', str(total_products)],
            ['Total Value', f"Rs. {total_value:.2f}"],
            ['In Stock', str(in_stock)],
            ['Out of Stock', str(out_of_stock)],
        ]
        
        summary_table = Table(summary_data, colWidths=[2*inch, 1.5*inch])
        summary_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10B981')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F0FDF4')),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#D1FAE5')),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        summary_table.setStyle(summary_style)
        story.append(summary_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_single_product_pdf(product):
    """
    Generate detailed PDF for a single product
    
    Args:
        product: Product object
    
    Returns:
        BytesIO buffer containing PDF data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1,
        textColor=colors.darkblue
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#4F46E5')
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        spaceAfter=6
    )
    
    story = []
    
    # Title
    story.append(Paragraph("Product Details", title_style))
    
    # Generated timestamp
    current_time = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    story.append(Paragraph(f"Generated on: {current_time}", normal_style))
    story.append(Spacer(1, 30))
    
    # Product details
    details_data = [
        ['Product Information', ''],
        ['Product ID', str(product.id)],
        ['Name', product.name],
        ['Category', product.category.name if product.category else 'N/A'],
        ['Price', f"Rs. {product.price:.2f}"],
        ['Status', product.get_status_display()],
        ['Description', product.description or 'No description available'],
        ['Created Date', product.created_at.strftime("%Y-%m-%d %H:%M:%S") if product.created_at else 'N/A'],
        ['Last Updated', product.updated_at.strftime("%Y-%m-%d %H:%M:%S") if product.updated_at else 'N/A'],
    ]
    
    details_table = Table(details_data, colWidths=[2*inch, 3*inch])
    details_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4F46E5')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#F9FAFB')),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ])
    details_table.setStyle(details_style)
    story.append(details_table)
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
