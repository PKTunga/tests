from django.db import models



class Packages(models.Model):
    price = models.DecimalField(max_digits=10, default=0.00, decimal_places=2)
    title = models.CharField(max_length=200, default="")
    features = models.TextField()
    template = models.ForeignKey('main.Templates', related_name='Template+', on_delete=models.SET_NULL, null=True, blank=True)
    
    
    def __str__(self):
        return f"{self.title} - {self.price}"
    
    
    

class Coupons(models.Model):
    value = models.DecimalField(max_digits=10, default=0.00, decimal_places=2)
    name = models.CharField(max_length=200, default="")
    description = models.TextField()
    package = models.ForeignKey('packages.Packages', related_name='Package+', on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.value}"