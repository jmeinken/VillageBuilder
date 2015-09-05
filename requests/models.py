from django.db import models
from account.models import Member

class Request(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    body = models.TextField()
    complete = models.BooleanField(default=False, db_index=True)
    
class RequestComment(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, db_index=True)
    body = models.TextField()
    #complete = models.BooleanField(default=False)
    

