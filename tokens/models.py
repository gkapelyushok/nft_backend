from django.db import models

class Token(models.Model):
    unique_hash = models.CharField(max_length=20, 
                                   unique=True, 
                                   blank=False, 
                                   null=False)
    tx_hash = models.CharField(max_length=66)
    media_url = models.URLField(blank=False, 
                                null=False)
    owner = models.CharField(max_length=42,
                             blank=False, 
                             null=False)