from datetime import datetime,date
from multiprocessing.dummy import current_process
from time import strftime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from carts.models import CartItem
from .forms import OrderForm
from .models import Order


def payments(request):
    return render(request,'orders/payments.html')


def place_order(request,total=0, quantity=0, cart_items=None):
    current_user = request.user

    # if cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')


    grand_total = 0
    tax =0 
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity
    tax = (16 * total)/100
    grand_total = total + tax 

    if request.method =='POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # store all info ->order table db
            data  = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.region = form.cleaned_data['region']
            data.city = form.cleaned_data['city']
            data.street = form.cleaned_data['street']
            data.pickup = form.cleaned_data['pickup']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()


            # generate order number
            yr = int(date.today().strftime('%Y'))
            dt = int(date.today().strftime('%d'))
            mt = int(date.today().strftime('%m'))
            d = date(yr,mt,dt)
            current_date = d.strftime("%Y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            return redirect('checkout')
        
        else:
            return redirect('checkout')




