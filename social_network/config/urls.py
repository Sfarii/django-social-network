"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path, include
from django.conf import settings
from django.contrib import admin

from django.views.generic.base import RedirectView, TemplateView

urlpatterns = [

    # Accounts URLs

    # Root-level redirects for common browser requests
    re_path(r'^favicon\.ico$', RedirectView.as_view(url=settings.STATIC_URL + 'img/compressed/favicon.ico'), name='favicon.ico'),
    re_path(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots.txt'),

    # Admin URLs
    re_path(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    re_path(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        # Testing 404 and 500 error pages
        re_path(r'^404/$', TemplateView.as_view(template_name='404.html'), name='404'),
        re_path(r'^500/$', TemplateView.as_view(template_name='500.html'), name='500'),
    ]

    try:
        from django.conf.urls.static import static
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

        import debug_toolbar
        urlpatterns += [
            re_path(r'^__debug__/', include(debug_toolbar.urls))
        ]

    # Should only occur when debug mode is on for production testing
    except ImportError as e:
        import logging
        l = logging.getLogger(__name__)
        l.warning(e)
