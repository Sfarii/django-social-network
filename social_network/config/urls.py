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

from django.urls import path, re_path, include, reverse_lazy
from django.conf import settings
from django.contrib import admin

from django.views.generic.base import RedirectView, TemplateView

urlpatterns = [

    # Auth app URLs
    path('auth/', include('apps.authentication.urls')),

    path('', RedirectView.as_view(url=reverse_lazy('login'))),

    # Account app URLs
    path('account/', include('apps.account.urls')),

    # blog app URLS
    path('blog/', include('apps.blog.urls')),

    # chat app URLS
    path('chat/', include('apps.chat.urls')),

    # Root-level redirects for common browser requests
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'img/brand/favicon.png'), name='favicon.ico'),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots.txt'),

    # Admin URLs
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        # Testing 404 and 500 error pages
        path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
        path('500/', TemplateView.as_view(template_name='500.html'), name='500'),
    ]

    try:
        from django.conf.urls.static import static
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

        import debug_toolbar
        urlpatterns += [
            re_path('__debug__/', include(debug_toolbar.urls))
        ]

    # Should only occur when debug mode is on for production testing
    except ImportError as e:
        import logging
        l = logging.getLogger(__name__)
        l.warning(e)
