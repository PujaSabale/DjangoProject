from django.contrib import admin
from django.urls import path
from Eshop import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home',views.home),
    path('user_login',views.user_login),
    path('user_logout',views.user_logout),
    path('register',views.register),
    path('product_details/<pid>',views.product_details),
    path('placeorder',views.placeorder),
    path('addtocart/<pid>',views.addtocart),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('viewcart',views.viewcart),
    path('remove/<cid>',views.remove),
    path('range',views.range),
    path('catfilter/<cv>',views.catfilter),
    path('makepayment',views.makepayment),
    path('contact',views.contact),
]


if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
