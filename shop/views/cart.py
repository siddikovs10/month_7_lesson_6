from django.shortcuts import render, redirect
from django.http import JsonResponse
from shop.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart:
            self.cart[product_id] += 1
        else:
            self.cart[product_id] = 1

        self.session.modified = True

    def remove(self, product_id):
        product_id = str(product_id)

        if product_id in self.cart.keys():
            del self.cart[product_id]
            self.session.modified = True
            return True
        return False

    def get_count(self):
        print(self.cart)
        return len(self.cart.keys())

    def get_products(self):
        products = []
        total_with_discount = 0

        for pid, quantity in self.cart.items():
            pd = Product.objects.get(id=pid)

            if pd.discount > 0:
                total = pd.discount_price * quantity
            else:
                total = pd.price * quantity
            total_with_discount += total
            product = {
                "quantity": quantity,
                "data": pd,
                "total": total
            }
            products.append(product)

        total_price = 0
        for pr in products:
            total_price += pr["data"].price * pr["quantity"]

        data = {
            "products": products,
            "total_price": total_price,
            "total_with_discount": total_with_discount,
            "profit": total_price - total_with_discount
        }

        return data
    
    def clear(self):
        self.cart.clear()
        self.session.modified = True

def add_to_cart(request, product_id):
    cart = Cart(request)
    
    if Product.objects.filter(id=product_id).exists():
        cart.add(product_id)
        
    return JsonResponse({'message': 'Product added to cart', 'cart_count': cart.get_count()})

def get_cart_page(request):
    cart = Cart(request)
    products = cart.get_products()

    data = {
        'path': 'Cart',
        'cart_count': cart.get_count(),
        'products': products
    }
    return render(request, 'shop/cart.html', context=data)

def del_cart_item(request, product_id):
    cart = Cart(request)
    products = cart.get_products()

    if cart.remove(product_id):
        return redirect('cart_page')

    data = {
        'path': 'Cart',
        'cart_count': cart.get_count(),
        'products': products
    }
    return render(request, 'shop/cart.html', context=data)
