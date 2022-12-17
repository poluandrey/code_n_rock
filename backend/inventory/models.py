from django.db import models


class File(models.Model):
    file_name = models.CharField(max_length=120)
    file = models.FileField(upload_to='audio/')
    insert_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name


class Product(models.Model):
    product_name = models.CharField(max_length=500, blank=True, null=True)
    product_number = models.IntegerField(blank=True, null=True)
    year = models.IntegerField(blank=True, null=True)
    factory = models.IntegerField(blank=True, null=True, default=None)
    comment = models.CharField(blank=True, max_length=500, null=True)

    def __str__(self):
        return self.product_name
