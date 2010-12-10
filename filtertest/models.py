from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Location(models.Model):
    company = models.ForeignKey(Company, related_name='locations')
    name = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    open_days = models.CharField(max_length=7)

    def __unicode__(self):
        return '%s: %s' % (self.company.name, self.name)
