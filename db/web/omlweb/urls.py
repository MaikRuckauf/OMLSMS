from django.conf.urls import patterns, include, url
from omlweb.views import home, summary, billing, results, billPDF, \
                            resultsPDF, invalidSterilizer

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    url(r'^$', home),
    
    url(r'^login/$', login, {'template_name': 'login.html'}),
    url(r'^logout/$', logout, {'next_page': '/login'}),
    
    url(r'^summary/$', summary),
    url(r'^billing/$', billing),
    url(r'^results/$', results),

    url(r'^billing/print_bill/(\d{3,5})$', billPDF),
    url(r'^results/print_results/(\d{3,5})$', resultsPDF),
    
    url(r'^invalid/sterilizer_id/(\d{3,5})$', invalidSterilizer),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
