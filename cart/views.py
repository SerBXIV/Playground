from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Book
from .cart import Cart, add_menu_to_context
from .forms import CartAddBookForm
from coupons.forms import CouponApplyForm

from coupons.models import Coupon


@require_POST
def cart_add(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)
    form = CartAddBookForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(book=book,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
    return redirect('cart:cart_detail')


def cart_remove(request, book_id):
    cart = Cart(request)
    book = get_object_or_404(Book, id=book_id)

    # перевірка, чи це купон
    if isinstance(book, Coupon):
        cart.remove(book)
    else:
        cart.remove(book)

    return redirect('cart:cart_detail')


@add_menu_to_context
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddBookForm(
            initial={'quantity': item['quantity'],
                     'update': True})
    coupon_apply_form = CouponApplyForm()
    return {'template_name': 'cart/detail.html',
            'cart': cart,
            'coupon_apply_form': coupon_apply_form}
