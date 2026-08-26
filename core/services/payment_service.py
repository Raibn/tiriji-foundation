import hashlib
import hmac
import json
import logging
import uuid

from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class GatewayError(Exception):
    """Raised when a payment gateway call fails."""


class PaymentService:
    METHOD_CONFIG = {
        'card': {
            'label': 'Card',
            'provider': 'Stripe Checkout',
            'action': 'Continue to card checkout',
            'instructions': [
                'Use this option for Visa, Mastercard, and other supported cards.',
                'You will be redirected to a secure Stripe-hosted checkout page.',
            ],
        },
        'stripe': {
            'label': 'Stripe',
            'provider': 'Stripe Checkout',
            'action': 'Continue to Stripe',
            'instructions': [
                'Use this option for card payments through Stripe.',
                'You will be redirected to a secure Stripe-hosted checkout page.',
            ],
        },
        'mpesa': {
            'label': 'M-Pesa',
            'provider': 'M-Pesa STK Push',
            'action': 'Send STK push',
            'instructions': [
                'Enter your M-Pesa registered phone number.',
                'You will receive a payment prompt directly on your phone.',
            ],
        },
        'paypal': {
            'label': 'PayPal',
            'provider': 'PayPal Checkout',
            'action': 'Continue to PayPal',
            'instructions': [
                'Use this option for PayPal wallet and supported international payments.',
                'You will be redirected to PayPal to approve the payment.',
            ],
        },
        'bank': {
            'label': 'Bank Transfer',
            'provider': 'Manual Bank Transfer',
            'action': 'Record bank transfer',
            'instructions': [
                'Transfer to Tiriji Foundation bank account using the reference shown below.',
                'Finance will reconcile the transfer from the admin portal once received.',
            ],
        },
    }

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    @classmethod
    def reference(cls, prefix='TIR'):
        return f'{prefix}-{uuid.uuid4().hex[:10].upper()}'

    @classmethod
    def method_config(cls, method):
        return cls.METHOD_CONFIG.get(method) or cls.METHOD_CONFIG['card']

    # -------------------------------------------------------------------------
    # Session builders (used by views to render the payment summary page)
    # -------------------------------------------------------------------------

    @classmethod
    def donation_session(cls, donation):
        method = donation.payment_method or 'mpesa'
        config = cls.method_config(method)
        reference = donation.payment_reference or cls.reference('PAY')

        if donation.transaction and not donation.transaction.transaction_reference:
            donation.transaction.transaction_reference = reference
            donation.transaction.save(update_fields=['transaction_reference'])

        if not donation.payment_reference:
            donation.payment_reference = reference
            donation.save(update_fields=['payment_reference'])

        return {
            'kind': 'donation',
            'method': method,
            'config': config,
            'reference': reference,
            'amount': donation.amount,
            'currency': donation.currency,
            'is_subscription': donation.is_monthly,
        }

    @classmethod
    def volunteer_session(cls, volunteer_payment, method='mpesa'):
        config = cls.method_config(method)
        reference = volunteer_payment.payment_reference or cls.reference('VOL')

        if not volunteer_payment.payment_reference:
            volunteer_payment.payment_reference = reference
            volunteer_payment.save(update_fields=['payment_reference'])

        if volunteer_payment.transaction:
            update_fields = []
            if volunteer_payment.transaction.payment_method != method:
                volunteer_payment.transaction.payment_method = method
                update_fields.append('payment_method')
            if not volunteer_payment.transaction.transaction_reference:
                volunteer_payment.transaction.transaction_reference = reference
                update_fields.append('transaction_reference')
            if update_fields:
                volunteer_payment.transaction.save(update_fields=update_fields)

        return {
            'kind': 'volunteer',
            'method': method,
            'config': config,
            'reference': reference,
            'amount': volunteer_payment.amount,
            'currency': 'USD',
            'is_subscription': False,
        }

    # -------------------------------------------------------------------------
    # Gateway initiation stubs
    # Each method returns a dict with `redirect_url` (for redirect-based flows)
    # or `checkout_request_id` (for STK push). Views use this to redirect the
    # user or display a waiting screen.
    # -------------------------------------------------------------------------

    @classmethod
    def initiate_stripe_checkout(cls, session_data, success_url, cancel_url):
        """
        TODO: Replace stub with live Stripe Checkout Session creation.

        Required env vars:
            STRIPE_SECRET_KEY      — sk_live_... (or sk_test_... for sandbox)
            STRIPE_PUBLISHABLE_KEY — pk_live_... (passed to frontend if needed)

        Live implementation (install stripe>=7 first):

            import stripe
            stripe.api_key = settings.STRIPE_SECRET_KEY
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': session_data['currency'].lower(),
                        'unit_amount': int(session_data['amount'] * 100),
                        'product_data': {'name': f"Tiriji Foundation — {session_data['kind'].title()} payment"},
                    },
                    'quantity': 1,
                }],
                mode='subscription' if session_data['is_subscription'] else 'payment',
                success_url=success_url + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=cancel_url,
                metadata={'reference': session_data['reference']},
            )
            return {'redirect_url': checkout_session.url, 'session_id': checkout_session.id}
        """
        raise GatewayError("Stripe Checkout is not yet configured. Set STRIPE_SECRET_KEY in environment.")

    @classmethod
    def initiate_paypal_order(cls, session_data, return_url, cancel_url):
        """
        TODO: Replace stub with live PayPal Orders API v2 call.

        Required env vars:
            PAYPAL_CLIENT_ID     — from developer.paypal.com
            PAYPAL_CLIENT_SECRET — from developer.paypal.com
            PAYPAL_MODE          — 'sandbox' or 'live'

        Live implementation (install paypalrestsdk or use httpx against the REST API):

            PayPal base URL:
              sandbox  → https://api-m.sandbox.paypal.com
              live     → https://api-m.paypal.com

            Steps:
              1. POST /v1/oauth2/token  (basic auth with client_id:secret, body: grant_type=client_credentials)
              2. POST /v2/checkout/orders with the order body below
              3. Extract approve_link from response links
              4. Redirect user to approve_link

            Order body:
                {
                  "intent": "CAPTURE",
                  "purchase_units": [{
                    "reference_id": session_data['reference'],
                    "amount": {"currency_code": session_data['currency'], "value": str(session_data['amount'])}
                  }],
                  "application_context": {"return_url": return_url, "cancel_url": cancel_url}
                }
        """
        raise GatewayError("PayPal Checkout is not yet configured. Set PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET.")

    @classmethod
    def initiate_mpesa_stk_push(cls, session_data, phone_number):
        """
        TODO: Replace stub with live Safaricom Daraja STK Push call.

        Required env vars:
            MPESA_CONSUMER_KEY    — from developer.safaricom.co.ke
            MPESA_CONSUMER_SECRET — from developer.safaricom.co.ke
            MPESA_SHORTCODE       — Business shortcode / paybill number
            MPESA_PASSKEY         — Lipa Na M-Pesa passkey from Safaricom portal
            MPESA_CALLBACK_URL    — Public HTTPS URL of the mpesa_callback view

        Live implementation (use httpx or requests):

            Daraja base URL:
              sandbox → https://sandbox.safaricom.co.ke
              live    → https://api.safaricom.co.ke

            Steps:
              1. GET /oauth/v1/generate?grant_type=client_credentials  (basic auth)
              2. Compute password: base64(shortcode + passkey + timestamp)
              3. POST /mpesa/stkpush/v1/processrequest with body:
                  {
                    "BusinessShortCode": settings.MPESA_SHORTCODE,
                    "Password": password,
                    "Timestamp": timestamp,
                    "TransactionType": "CustomerPayBillOnline",
                    "Amount": int(session_data['amount']),
                    "PartyA": phone_number,   # 254XXXXXXXXX format
                    "PartyB": settings.MPESA_SHORTCODE,
                    "PhoneNumber": phone_number,
                    "CallBackURL": settings.MPESA_CALLBACK_URL,
                    "AccountReference": session_data['reference'],
                    "TransactionDesc": "Tiriji Foundation placement fee",
                  }
              4. Store CheckoutRequestID against the transaction reference
              5. Return checkout_request_id for polling / callback matching
        """
        raise GatewayError("M-Pesa STK Push is not yet configured. Set MPESA_CONSUMER_KEY and related env vars.")

    # -------------------------------------------------------------------------
    # Completion helpers (called by webhook handlers once payment is confirmed)
    # -------------------------------------------------------------------------

    @classmethod
    def complete_donation(cls, donation):
        donation.status = 'completed'
        donation.amount_paid = donation.amount
        donation.payment_date = timezone.now()
        if not donation.payment_reference:
            donation.payment_reference = cls.reference('PAY')
        donation.save(update_fields=['status', 'amount_paid', 'payment_date', 'payment_reference'])

        if donation.transaction:
            donation.transaction.status = 'paid'
            donation.transaction.transaction_reference = donation.payment_reference
            donation.transaction.save(update_fields=['status', 'transaction_reference'])

    @classmethod
    def complete_volunteer_payment(cls, volunteer_payment):
        volunteer_payment.paid = True
        if not volunteer_payment.payment_reference:
            volunteer_payment.payment_reference = cls.reference('VOL')
        volunteer_payment.save(update_fields=['paid', 'payment_reference'])

        volunteer_payment.transaction.status = 'paid'
        volunteer_payment.transaction.transaction_reference = volunteer_payment.payment_reference
        volunteer_payment.transaction.save(update_fields=['status', 'transaction_reference'])

        volunteer_payment.volunteer.status = 'paid'
        volunteer_payment.volunteer.save(update_fields=['status'])

    # -------------------------------------------------------------------------
    # Webhook handlers — called from the webhook views in views.py
    # Each returns True if the event was handled, False if it should be ignored.
    # Raises GatewayError on signature / parsing failure.
    # -------------------------------------------------------------------------

    @classmethod
    def handle_stripe_webhook(cls, payload_bytes, sig_header):
        """
        Verify the Stripe webhook signature and dispatch to the right handler.

        TODO: Replace the stub body with the live implementation once
              STRIPE_WEBHOOK_SECRET is set in environment.

        Live implementation:
            import stripe
            try:
                event = stripe.Webhook.construct_event(
                    payload_bytes, sig_header, settings.STRIPE_WEBHOOK_SECRET
                )
            except stripe.error.SignatureVerificationError:
                raise GatewayError("Invalid Stripe webhook signature")

            if event['type'] == 'checkout.session.completed':
                session = event['data']['object']
                reference = session['metadata'].get('reference')
                cls._fulfill_by_reference(reference)
                return True

            # Ignored event type
            return False
        """
        raise GatewayError("Stripe webhook handler not yet implemented. Set STRIPE_WEBHOOK_SECRET.")

    @classmethod
    def handle_paypal_webhook(cls, payload_bytes, headers):
        """
        Verify the PayPal webhook signature and dispatch.

        TODO: Replace the stub body once PAYPAL_WEBHOOK_ID is set.

        Live implementation:
            Verify via POST to /v1/notifications/verify-webhook-signature
            using paypal_auth_algo, cert_url, transmission_id, etc. from headers.

            If event_type == 'PAYMENT.CAPTURE.COMPLETED':
                reference = event['resource']['custom_id']  # set during order creation
                cls._fulfill_by_reference(reference)
                return True
            return False
        """
        raise GatewayError("PayPal webhook handler not yet implemented.")

    @classmethod
    def handle_mpesa_callback(cls, result_data):
        """
        Parse the Safaricom STK Push callback and fulfill the matching transaction.

        TODO: This will work once the STK push initiation is live, because
              Safaricom will POST this to /webhooks/mpesa/ automatically.

        Callback shape:
            {
              "Body": {
                "stkCallback": {
                  "ResultCode": 0,          # 0 = success
                  "ResultDesc": "Success",
                  "CheckoutRequestID": "...",
                  "CallbackMetadata": {
                    "Item": [
                      {"Name": "Amount", "Value": 1600},
                      {"Name": "MpesaReceiptNumber", "Value": "NLJ7RT61SV"},
                      {"Name": "PhoneNumber", "Value": 254700000000}
                    ]
                  }
                }
              }
            }

        Live implementation:
            callback = result_data.get('Body', {}).get('stkCallback', {})
            if callback.get('ResultCode') != 0:
                logger.warning("M-Pesa STK failed: %s", callback.get('ResultDesc'))
                return False

            checkout_request_id = callback['CheckoutRequestID']
            # Look up the transaction by CheckoutRequestID stored during initiation:
            from core.models import Transaction
            try:
                txn = Transaction.objects.get(transaction_reference=checkout_request_id)
            except Transaction.DoesNotExist:
                raise GatewayError(f"No transaction for CheckoutRequestID {checkout_request_id}")

            txn.status = 'paid'
            txn.save(update_fields=['status'])

            # Fulfill the related object (VolunteerPayment or donation)
            if hasattr(txn, 'volunteer_payment'):
                cls.complete_volunteer_payment(txn.volunteer_payment)
            elif hasattr(txn, 'donation'):
                cls.complete_donation(txn.donation)
            return True
        """
        raise GatewayError("M-Pesa callback handler not yet implemented.")

    # -------------------------------------------------------------------------
    # Internal helper — look up and fulfill any payment by reference string
    # -------------------------------------------------------------------------

    @classmethod
    def _fulfill_by_reference(cls, reference):
        """Find a pending transaction by reference and mark it complete."""
        if not reference:
            raise GatewayError("Empty payment reference")

        from core.models import Transaction
        try:
            txn = Transaction.objects.select_related(
                'volunteer_payment__volunteer', 'donation'
            ).get(transaction_reference=reference, status='pending')
        except Transaction.DoesNotExist:
            logger.warning("PaymentService: no pending transaction for reference %s", reference)
            return

        if hasattr(txn, 'volunteer_payment'):
            cls.complete_volunteer_payment(txn.volunteer_payment)
        elif hasattr(txn, 'donation'):
            cls.complete_donation(txn.donation)
        else:
            txn.status = 'paid'
            txn.save(update_fields=['status'])
