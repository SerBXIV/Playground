from decimal import Decimal
from django.conf import settings
from django.shortcuts import render
from coupons.models import Coupon
from shop.models import Book, Genre, Section

def add_menu_to_context(view_func):
    """
    Декоратор, який додає до контексту навігаційне меню розділів та жанрів.
    """
    def wrapper(request, *args, **kwargs):
        context = view_func(request, *args, **kwargs)
        context['genres'] = Genre.objects.all()
        context['sections'] = Section.objects.all()
        return render(request, context['template_name'], context)

    return wrapper

class Cart(object):

    def __init__(self, request):
        """
        Ініціалізуємо корзину
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get('coupon_id')

    def add(self, book, quantity=1, update_quantity=False):
        """
        Додати книги в корзину або оновити їх кількість.
        """
        book_id = str(book.id)
        if book_id not in self.cart:
            self.cart[book_id] = {'quantity': 0,
                                     'price': str(book.price)}
        if update_quantity:
            self.cart[book_id]['quantity'] = quantity
        else:
            self.cart[book_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Оновлення сесії cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Відмітити сеанс як "змінений", щоб переконатися, що його збережено
        self.session.modified = True

    def remove(self, book):
        """
        Видалення товару з корзини.
        """
        book_id = str(book.id)
        if book_id in self.cart:
            del self.cart[book_id]
            self.save()


    def __iter__(self):
        """
        Перебір елементів в корзині і отримання книг з БД.
        """
        book_ids = self.cart.keys()
        # отримання об’єктів book та додавання їх до корзини
        books = Book.objects.filter(id__in=book_ids)
        for book in books:
            self.cart[str(book.id)]['book'] = book

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Підрахунок кількості товарів в корзині.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Підрахунок вартості товарів в корзині.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in
                   self.cart.values())

    def clear(self):
        # видалення корзини з сесії
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal('100')) * self.get_total_price()
        return Decimal('0')

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()