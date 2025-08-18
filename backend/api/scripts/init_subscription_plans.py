#!/usr/bin/env python3
"""
初始化订阅计划脚本
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from api.extensions.database import db
from api.data.models.subscription import SubscriptionPlan
from api.api_app import create_app


def init_subscription_plans():
    """初始化默认订阅计划"""
    app = create_app()

    with app.app_context():
        # 检查是否已有计划
        existing_plans = SubscriptionPlan.query.all()
        if existing_plans:
            print("Subscription plans already exist, skipping initialization.")
            return

        # 创建默认计划
        plans = [
            {
                "name": "free",
                "price": 0,
                "interval": "monthly",
                "interval_count": 1,
                "stripe_price_id": "",
                "credit_amount": 0,
                # "duration_days": 30,
                "is_active": True,
                "created_by": 1,
                "updated_by": 1,
            },
            {
                "name": "pro",
                "price": 1000,  # $10.00
                "interval": "monthly",
                "interval_count": 1,
                "stripe_price_id": "price_1RwCoMP089RcvSY1barkpo7F",
                "credit_amount": 500,
#                 "duration_days": 30,
                "is_active": True,
                "created_by": 1,
                "updated_by": 1,
            },
            {
                "name": "ultra",
                "price": 2000,  # $20.00
                "interval": "monthly",
                "interval_count": 1,
                "stripe_price_id": "",
                "credit_amount": 1200,
#                 "duration_days": 30,
                "is_active": True,
                "created_by": 1,
                "updated_by": 1,
            },
        ]

        for plan_data in plans:
            plan = SubscriptionPlan(**plan_data)
            db.session.add(plan)
            print(
                f"Created plan: {plan.name} - ${plan.price / 100:.2f} - {plan.credit_amount} credits"
            )

        db.session.commit()
        print("Subscription plans initialized successfully!")


if __name__ == "__main__":
    init_subscription_plans()
