from django.db import models

from django_fsm import FSMField, transition

from account.models import Account


class File(models.Model):
    file_name = models.CharField(max_length=120)
    file = models.FileField(upload_to='audio/')
    insert_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='files', null=True)

    def __str__(self):
        return self.file_name


class ParsingStatus(models.Model):
    status = FSMField(default='in progress')
    file = models.OneToOneField(File, on_delete=models.CASCADE, related_name='status')
    insert_date = models.DateTimeField(auto_now_add=True)

    @transition('status', source='in progress', target='finished')
    def finished(self):
        pass

    def __str__(self):
        return self.status
