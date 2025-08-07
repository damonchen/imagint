from enum import StrEnum
from api.libs.language import LanguageEnumValue


class AccountStatus(StrEnum):
    PENDING = "pending"
    UNINITIALIZED = "uninitialized"
    ACTIVE = "active"
    RESET_PASSWORD = "reset_password"
    BANNED = "banned"
    CLOSED = "closed"

    @staticmethod
    def value_of(value):
        for member in AccountStatus:
            if member.value == value:
                return member
        return ValueError("not matching enum found for value: {}".format(value))

    def get_display_name(self, language):
        m = {
            "pending": LanguageEnumValue(
                "pending", {"en-US": "Pending", "zh-CN": "待激活"}
            ),
            "uninitialized": LanguageEnumValue(
                "uninitialized", {"en-US": "Uninitialized", "zh-CN": "未初始化"}
            ),
            "active": LanguageEnumValue("active", {"en-US": "Active", "zh-CN": "激活"}),
            "reset_password": LanguageEnumValue(
                "reset_password", {"en-US": "ResetPassword", "zh-CN": "重置密码"}
            ),
            "banned": LanguageEnumValue("banned", {"en-US": "Banned", "zh-CN": "禁用"}),
            "closed": LanguageEnumValue(
                "closed", {"en-US": "Closed", "zh-CN": "已关闭"}
            ),
        }
        return m[self.value].get_display_name(language)


class OAuthProvider(StrEnum):
    WECHAT = "wechat"
    GOOGLE = "google"


class SubscriptionStatus(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class OrderStatus(StrEnum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class TaskStatus(StrEnum):
    PENDING = "pending"
    CANCELLED = "cancelled"
    SUCCESS = "success"
    FAILED = "failed"
    RUNNING = "running"


class TaskWebTokenStatus(StrEnum):
    ACTIVE = "active"
    DISABLED = "disabled"

    @staticmethod
    def value_of(value):
        for member in TaskWebTokenStatus:
            if member.value == value:
                return member
        return ValueError("not matching enum found for value: {}".format(value))
