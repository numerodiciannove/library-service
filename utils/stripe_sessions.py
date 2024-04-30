import os

import stripe.checkout
from borrowings_app.models import Borrowing
from dotenv import load_dotenv
from payments_app.models import Payment

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


def create_stripe_checkout_session(product_name: str, price: int):
    session = stripe.checkout.Session.create(
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product_name,
                    },
                    "unit_amount": price,
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://localhost:8000/success",
        cancel_url="http://localhost:8000/cancel",
    )

    return session


def create_payment(borrowing: Borrowing, payment_type: str) -> Payment:
    borrowing_book_title = borrowing.book.title
    borrowing_total_price = int(
        (
                (borrowing.expected_return_date - borrowing.borrow_date).days
                * borrowing.book.daily_fee
        )
        * 100
    )

    stripe_session = create_stripe_checkout_session(
        product_name=borrowing_book_title, price=borrowing_total_price
    )

    payment = Payment.objects.create(
        status="PENDING",
        type=payment_type.upper(),
        borrowing=borrowing,
        session_url=stripe_session.url,
        session_id=stripe_session.id,
        money_to_pay=borrowing_total_price,
    )

    return payment
