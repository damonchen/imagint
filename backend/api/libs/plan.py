from api.extensions.database import db


class Plan(object):

    def verify(self, account) -> bool:
        raise NotImplemented()


class NoPlan(Plan):

    def verify(self, account) -> bool:
        return True


class Sequence(Plan):

    def __init__(self, plans) -> None:
        super().__init__()
        self.plans = plans

    def verify(self, account) -> bool:
        for plan in self.plans:
            if not plan.verify():
                return False
        return True


class AccountPlan(Plan):

    def verify(self, account) -> bool:
        db.session.query()


class MonthPlan(Plan):
    pass


try_plan = None
normal_plan = None
advanced_plan = None


def plan_subscription_decorator():
    pass
