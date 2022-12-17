import csv
import xlwt
from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets

from .models import File, Product
from .serializers import ProductSerializer, FileUploadSerializer, FileSerializer

from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.http import HttpResponse


class FileUploadView(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.all()
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            files = serializer.save()
            data = {'detail': files, 'status': True}
            return Response(data=data, status=status.HTTP_201_CREATED)
        data = {"detail": serializer.errors, 'status': False}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)


fs = FileSystemStorage(location='tmp/')

def upload_data(file):

    content = file.read()

    file_content = ContentFile(content)
    file_name = fs.save(
        "tmp.csv", file_content
    )
    tmp_file = fs.path(file_name)

    csv_file = open(tmp_file, encoding='cp1251', errors="ignore")
    reader = csv.reader(csv_file, delimiter=",")
    next(reader)

    product_list = []

    for id_, row in enumerate(reader):

        (
            product_name,
            product_number,
            year,
            factory,
            comment,
        ) = row
        if product_number == "":
            product_number = None
        if year == "":
            year = None
        if factory == "":
            factory = None
        product_list.append(
            Product(
                product_name=product_name,
                product_number=product_number,
                year=year,
                factory=factory,
                comment=comment,
            )
        )

    Product.objects.bulk_create(product_list)

    return Response("Успешно загрузили таблицу")


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['POST'])
    def upload_data(self, request, file=None):
        if not file:
            file = request.FILES["file"]

        upload_data(file=file)


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="products.xls"'

    wb = xlwt.Workbook(encoding='cp1251')
    ws = wb.add_sheet('Product')

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Название', 'Номер', 'Год', 'Завод', 'Комментарии']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = Product.objects.all().values_list('product_name', 'product_number', 'year',
                                             'factory', 'comment')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
