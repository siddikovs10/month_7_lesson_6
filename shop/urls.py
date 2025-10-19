from django.urls import path
from shop.views import dashboard, detail, login_user, logout_user, profile_user, shop_page, get_products_with_category, register_user, add_to_cart, get_cart_page, del_cart_item, GetCheckoutPageView

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('detail/', detail, name='detail'),

    path('profile/', profile_user, name='profile'),
    path('shop/', shop_page, name='shop'),
    path('category/<int:pk>/', get_products_with_category, name='category_products'),

    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', get_cart_page, name='cart_page'),
    path('cart/remove/<int:product_id>/', del_cart_item, name='remove_cart_item'),

    path('login/', login_user, name='login_user'),
    path('logout/', logout_user, name='logout_user'),
    path('register/', register_user, name='register_user'),

    path('checkout/', GetCheckoutPageView.as_view(), name='checkout'),
]