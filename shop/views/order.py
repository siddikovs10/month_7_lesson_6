from django.shortcuts import render, redirect
from django.views.generic import View
from shop.models import OrderItem, Order
from shop.views import Cart
from django.contrib.auth.mixins import LoginRequiredMixin

class GetCheckoutPageView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        products = cart.get_products()
        data = {
            "path": "Checkout",
            "cart_count": cart.get_count(),
            "products": products,
        }
        return render(request, "shop/checkout.html", context=data)
    
    def post(self, request):
        user = request.user
        cart = Cart(request)
        products = cart.get_products()
        address = request.POST.get('address', "No address")
        additional = request.POST.get('additional', "No additional info")

        items = []

        for product in products["products"]:
            item, created = OrderItem.objects.get_or_create(
                product=product['data'],
                quantity=product['quantity'],
                total_price=product['total']
            )
            items.append(item)
        order = Order(user=user, address=address, additional_info=additional)
        order.save()
        order.items.add(*items)
        cart.clear()

        return redirect('dashboard')