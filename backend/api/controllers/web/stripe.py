import logging
import json
from flask import request, current_app, jsonify, render_template
from flask_restful import Resource
from api.extensions.stripe import stripe
from api.services.stripe_service import StripeService

from . import bp

logger = logging.getLogger(__name__)


@bp.route("/stripe/callback", methods=["POST"])
def stripe_callback():
    signature = request.headers.get("Stripe-Signature")
    payload = request.data

    logger.info("stripe callback %s", payload)

    try:
        event = stripe.Webhook.construct_event(
            payload, signature, current_app.config["STRIPE_WEBHOOK_SECRET"]
        )
    except ValueError as e:
        return "Invalid payload", 400
    except stripe.error.SignatureVerificationError as e:
        return "Invalid signature", 400

    type = event["type"]
    with open(f"/tmp/{type}.json", "w") as fp:
        fp.write(json.dumps(event, indent=4, ensure_ascii=False))

    logger.info("stripe callback event %s", event)

    # 处理订阅相关事件
    if event["type"] == "customer.subscription.created":
        subscription = event["data"]["object"]
        StripeService.handle_subscription_created(subscription, payload)

    elif event["type"] == "customer.subscription.updated":
        subscription = event["data"]["object"]
        StripeService.handle_subscription_updated(subscription, payload)

    elif event["type"] == "invoice.payment_succeeded":
        invoice = event["data"]["object"]
        StripeService.handle_payment_succeeded(invoice, payload)

    elif event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        StripeService.handle_subscription_canceled(subscription, payload)

    return jsonify({"status": "success"}), 200


@bp.route("/stripe/success")
def stripe_success():
    session_id = request.args.get("session_id")
    if not session_id:
        return "缺少session_id参数", 400

    # 系统支付成功，会回调到此处，此时应该显示网页内容，然后过一会儿跳转到后台中
    logger.info("stripe success %s", session_id)
    try:
        # 获取完整的session详情
        session = stripe.checkout.Session.retrieve(
            session_id, expand=["customer", "subscription"]  # 展开相关对象
        )

        logger.info("stripe session %s", session)

        # 提取重要信息
        customer_email = session.customer.email
        metadata = session.customer.metadata

        logger.info("session customer data %s, %s", customer_email, metadata)

        user_id = int(metadata["user_id"])

        subscription_id = session.subscription.id
        payment_status = session.payment_status

        return render_template(
            "web/stripe/success.html",
            **{
                "customer_email": customer_email,
                "subscription_id": subscription_id,
                "payment_status": payment_status,
            },
        )

        # return f"""
        #         <h1>支付成功！</h1>
        #         <p>客户邮箱: {customer_email}</p>
        #         <p>订阅ID: {subscription_id}</p>
        #         <p>支付状态: {payment_status}</p>
        #     """

    except stripe.error.StripeError as e:
        return f"Stripe错误: {str(e)}", 400


@bp.route("/stripe/cancel")
def stripe_cancel():
    pass
