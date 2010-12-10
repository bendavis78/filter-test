from filtertest import models
from django.contrib import admin
from django.contrib.admin.filterspecs import FilterSpec
from django.utils.datastructures import SortedDict

class CompanyOpenFilterSpec(FilterSpec):
    def __init__(self, request, params, model, model_admin):
        super(CompanyOpenFilterSpec, self).__init__(request, params, model, model_admin)
        self.links = SortedDict((
            ('Any', 'open_any'),
            ('Weekdays', 'open_weedays'),
            ('Weekends', 'open_weekends'),
        ))
        
    def consumed_params(self):
        return self.links.values()
    
    def choices(self, cl):
        selected = [v for v in self.links.values() if self.params.has_key(v)]
        for title, key in self.links.items():
            yield {'selected': (self.params.has_key(key) or (key=='open_any' and selected==[])),
                   'query_string': cl.get_query_string({key:1}, selected),
                   'display': title}
    
    def get_query_set(self, cl, qs):
        if self.params.has_key('open_weedays'):
            return qs.filter(locations__open_days__contains='12345').distinct()
        if self.params.has_key('open_weekends'):
            return qs.filter(locations__open_days__contains='67').distinct()
        return qs
    
    def title(self):
        return u'Locations open?'


class ZipCodeFilterSpec(FilterSpec):
    def __init__(self, request, params, model, model_admin):
        super(ZipCodeFilterSpec, self).__init__(request, params, model, model_admin)
        self.links = SortedDict((
            ('Any', 'zip_any'),
            ('90***', 'zip_90'),
            ('75***', 'zip_75'),
        ))

    def consumed_params(self):
        return self.links.values()

    def choices(self, cl):
        selected = [v for v in self.links.values() if self.params.has_key(v)]
        for title, key in self.links.items():
            yield {'selected': (self.params.has_key(key) or (key=='zip_any' and selected==[])),
                   'query_string': cl.get_query_string({key:1}, selected),
                   'display': title}
    
    def get_query_set(self, cl, qs):
        if self.params.has_key('zip_90'):
            return qs.filter(locations__zip_code__startswith='90').distinct()
        if self.params.has_key('zip_75'):
            return qs.filter(locations__zip_code__startswith='75').distinct()
        return qs

    def title(self):
        return u'Zip code'


class LocationInline(admin.StackedInline):
    model = models.Location

class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', '_locations', '_zips', '_days']
    list_filter = [CompanyOpenFilterSpec, ZipCodeFilterSpec]
    inlines = [LocationInline]

    def _locations(self, obj):  
        return ', '.join([l.name for l in obj.locations.all()])
    
    def _zips(self, obj):
        return ', '.join([l.zip_code for l in obj.locations.all()])

    def _days(self, obj):
        return ', '.join([l.open_days for l in obj.locations.all()])

admin.site.register(models.Company, CompanyAdmin)
