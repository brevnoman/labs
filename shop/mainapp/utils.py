

def recalc_cart(cart):
    if cart.pk:
        all_products = cart.products.all()
        products_count = 0
        products_price = 0
        for product in all_products:
            products_count += product.qty
            products_price += product.final_price
        cart.total_products = products_count
        cart.final_price = products_price
    cart.save()