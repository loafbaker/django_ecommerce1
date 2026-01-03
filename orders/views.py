import stripe

from django.shortcuts import render, HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

# Create your views here.
from accounts.models import UserAddress
from accounts.forms import UserAddressForm
from carts.models import Cart
from .models import Order
from .utils import id_generator

try:
    stripe_pub = settings.STRIPE_PUBLISHABLE_KEY
    stripe_secret = settings.STRIPE_SECRET_KEY
except Exception as e:
    raise NotImplementedError(str(e))

stripe.api_key = stripe_secret

def orders(request):
    context = {}
    template = "orders/user.html"
    return render(request, template, context)

# require user login
@login_required
def checkout(request):

    try:
        the_id = request.session['cart_id']
        cart = Cart.objects.get(id=the_id)
    except:
        the_id = None
        return HttpResponseRedirect(reverse("cart"))

    try:
        new_order = Order.objects.get(cart=cart)
    except Order.DoesNotExist:
        new_order = Order()
        new_order.cart = cart
        new_order.user = request.user
        new_order.order_id = id_generator()
        new_order.save()
    except:
        new_order = None
        # work on some error messages
        return HttpResponseRedirect(reverse("cart"))

    final_amount = 0
    if new_order is not None:
        new_order.sub_total = cart.total
        new_order.save()
        final_amount = new_order.get_final_amount()

    address_form = UserAddressForm()
    try:
        address_added = request.GET.get('address_added')
    except:
        address_added = None

    if address_added is None:
       address_form = UserAddressForm()
    else:
       address_form = None

    current_addresses = UserAddress.objects.filter(user=request.user)
    billing_addresses = UserAddress.objects.get_billing_address(user=request.user)
    # assign an address
    # run credit card

    if request.method == "POST":
        try:
            user_stripe = request.user.userstripe.stripe_id
            customer = stripe.Customer.retrieve(user_stripe)
            print(customer)
        except:
            customer = None

        if customer is not None:
            shipping_a = request.POST['shipping_address']
            billing_a = request.POST['billing_address']
            token = request.POST['stripeToken']

            try:
                shipping_address_instance = UserAddress.objects.get(id=shipping_a)
            except:
                shipping_address_instance = None
            try:
                billing_address_instance = UserAddress.objects.get(id=billing_a)
            except:
                billing_address_instance = None

            card = stripe.Customer.create_source(customer.id, source=token)
            card.address_city = billing_address_instance.city or None
            card.address_country = billing_address_instance.country or None
            card.address_line1 = billing_address_instance.address or None
            card.address_line2 = billing_address_instance.address2 or None
            card.address_state = billing_address_instance.state or None
            card.address_zip = billing_address_instance.zipcode or None
            card.save()

            charge = stripe.Charge.create(
                amount=int(final_amount * 100),
                currency="usd",
                source=card, # obtained with Stripe.js
                customer=customer,
                description="Charge for %s" % (request.user.username)
            )
            print(card)
            print(charge)
            if charge['captured']:
                new_order.status = 'Finished'
                new_order.shipping_address = shipping_address_instance
                new_order.billing_address = billing_address_instance
                new_order.save()
                # cart.delete()
                del request.session['cart_id']
                del request.session['items_total']
                messages.success(request, 'Thank you for your order. Your order has been completed!')
                return HttpResponseRedirect(reverse("user_orders"))

    context = {
        'order': new_order,
        'address_form': address_form,
        'current_addresses': current_addresses,
        'billing_addresses': billing_addresses,
        'stripe_pub': stripe_pub
    }
    template = "orders/checkout.html"
    return render(request, template, context)
