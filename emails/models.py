from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Booking(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    services = models.ManyToManyField(Service)  # Better way to store multiple services
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        services_list = ', '.join([service.name for service in self.services.all()])
        return f'{self.name} - {services_list} on {self.date} at {self.time}'
