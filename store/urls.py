from django.urls import path

from . import views

urlpatterns = [
        #Leave as empty string for base url
	path('', views.index, name="home"),
	path('store/', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('about/', views.about, name="about"),
	path('contacts/', views.contacts, name="contacts"),
	path('checkout/', views.checkout, name="checkout"),
	path('store/<int:pk>', views.ItemsDetailView.as_view(), name='item'),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
	path('privacy/', views.privacy, name="privacy"),
	path('checkoutthx/', views.checkoutthx, name="checkoutthx"),
	path('search/', views.search, name='search'),
	# path('threed/', views.threed, name="threed"),
    ]

