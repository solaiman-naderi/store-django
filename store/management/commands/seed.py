from django.core.management.base import BaseCommand
from model_bakery import baker
import random
from faker import Faker
from store.models import (
    Collection,
    Promotion,
    Product,
    Customer,
    Order,
    OrderItem,
    Address,
    Cart,
    CartItem,
)

fake = Faker("fa_IR")  # فارسی


class Command(BaseCommand):
    help = "Reset and seed database with realistic fake data"

    def handle(self, *args, **options):
        # ---- پاک کردن داده‌ها ----
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Address.objects.all().delete()
        Product.objects.all().delete()
        Promotion.objects.all().delete()
        Collection.objects.all().delete()
        Customer.objects.all().delete()

        self.stdout.write("🗑️  All previous data deleted!")

        # ---- Collections ----
        collections = [baker.make(Collection, title=fake.word())
                       for _ in range(5)]

        # ---- Promotions ----
        promotions = [baker.make(Promotion, description=fake.sentence(
        ), discount=random.uniform(5, 50)) for _ in range(5)]

        # ---- Products ----
        products = []
        for _ in range(20):
            collection = random.choice(collections)
            product = baker.make(
                Product,
                title=fake.word(),
                slug=fake.slug(),
                description=fake.text(max_nb_chars=200),
                unit_price=round(random.uniform(10, 1000), 2),
                inventory=random.randint(1, 500),
                collection=collection
            )
            product.promotion.add(*random.sample(promotions, k=2))
            products.append(product)

        # ---- Customers ----
        customers = []
        for _ in range(10):
            customers.append(
                baker.make(
                    Customer,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.unique.email(),
                    phone=fake.phone_number(),
                    birth_date=fake.date_of_birth(),
                    membership=random.choice(["B", "S", "G"])
                )
            )

        # ---- Orders & OrderItems ----
        orders = []
        for _ in range(10):
            customer = random.choice(customers)
            order = baker.make(
                Order,
                customer=customer,
                payment_status=random.choice(["P", "C", "F"])
            )
            orders.append(order)
            for _ in range(random.randint(1, 5)):
                baker.make(
                    OrderItem,
                    order=order,
                    product=random.choice(products),
                    quantity=random.randint(1, 10),
                    unit_price=random.choice(products).unit_price
                )

        # ---- Addresses ----
        for _ in range(10):
            baker.make(
                Address,
                customer=random.choice(customers),
                street=fake.street_address(),
                city=fake.city()
            )

        # ---- Carts & CartItems ----
        carts = baker.make(Cart, _quantity=5)
        for cart in carts:
            for _ in range(random.randint(1, 5)):
                baker.make(
                    CartItem,
                    cart=cart,
                    product=random.choice(products),
                    quantity=random.randint(1, 10)
                )

        self.stdout.write(self.style.SUCCESS(
            "✅ Database reset and seeded with realistic data!"))
