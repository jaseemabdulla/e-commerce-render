from django.shortcuts import render
from cart.models import Order
from datetime import datetime
from product.models import Product,ProductVariant

from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from openpyxl import Workbook
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required(login_url='user_login')
def sales_report(request):
    
    orders = Order.objects.filter(status = 'DELIVERED').order_by('-updated_at')
    
    if request.method == 'POST':
        
        start_date_str = request.POST.get('start_date')
        end_date_str = request.POST.get('end_date')
        download_format = request.POST.get('download_format')
        
        if start_date_str and end_date_str and download_format:
            
            start_date = datetime.strptime(start_date_str,'%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str,'%Y-%m-%d').date()
            
            orders = Order.objects.filter(status = 'DELIVERED',updated_at__range=(start_date,end_date)).order_by('-updated_at')
            
            if download_format == 'pdf':
                return download_pdf(request, orders)
                
            if download_format == 'excel':
                return download_excel(request,orders)
          
        else:
            orders = Order.objects.filter(status = 'DELIVERED').order_by('-updated_at')
            
        
            
    
    context = {
        'orders':orders
    }
    
    
    return render(request,'c_admin/sales_report.html',context)


def generate_pdf(response, data):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#808080'),
                        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), (217 / 255.0, 227 / 255.0, 243 / 255.0)),
                        ('GRID', (0, 0), (-1, -1), 1, (0.5, 0.5, 0.5))])

    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

def generate_excel(data):
    wb = Workbook()
    ws = wb.active

    for row in data:
        ws.append(row)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sales_report.xlsx'
    wb.save(response)
    return response


def download_pdf(request,orders):
    data = [['Order ID', 'Customer', 'Total Amount','payment_method', 'Date']]
    for order in orders:
        updated_at_formatted = order.updated_at.strftime('%d-%m-%Y')
        data.append([order.id, order.user.username, order.total_price,order.payment_method, updated_at_formatted])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
    generate_pdf(response, data)
    return response

def download_excel(request,orders):
    data = [['Order ID', 'Customer', 'Total Amount','payment_method', 'Date']]
    for order in orders:
        updated_at_formatted = order.updated_at.strftime('%d-%m-%Y')
        data.append([order.id, order.user.username, order.total_price,order.payment_method, updated_at_formatted])
    response = generate_excel(data)
    return response


# stock report
@login_required(login_url='user_login')
def stock_report(request):
    
    if request.method == 'POST':
        
        download_format = request.POST.get('download_format')
        
        if download_format:
            
            products = ProductVariant.objects.all()
            
            if download_format == 'pdf':
                return download_pdf_stock(request, products)
                
            if download_format == 'excel':
                return download_excel_stock(request,products)
          


def generate_pdf_stock(response, data):
    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    elements = []

    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#808080'),
                        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), (217 / 255.0, 227 / 255.0, 243 / 255.0)),
                        ('GRID', (0, 0), (-1, -1), 1, (0.5, 0.5, 0.5))])

    table.setStyle(style)
    elements.append(table)
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

def generate_excel_stock(data):
    wb = Workbook()
    ws = wb.active

    for row in data:
        ws.append(row)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=stock_report.xlsx'
    wb.save(response)
    return response


def download_pdf_stock(request,products):
    data = [['Product Name', 'Variant', 'Price','Stock']]
    for product in products:
        
        data.append([product.product.name, product.material, product.price,product.stock_quantity])

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="stock_report.pdf"'
    generate_pdf_stock(response, data)
    return response

def download_excel_stock(request,products):
    data = [['Product Name', 'Variant', 'Price','Stock']]
    for product in products:
        
        data.append([product.product.name, product.material, product.price,product.stock_quantity])
    response = generate_excel_stock(data)
    return response