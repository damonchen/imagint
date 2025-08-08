import time
import json
from api.services.mail_service import MailService
from api.services.redis_service import RedisService

while True:
    try:
        key = 'mail:account:register'
        value = RedisService.rpush(key)
        account_info = json.loads(value)

        token = account_info['token']

        MailService.send_register_token_mail(account_info, token)
    except KeyboardInterrupt:
        break
    except Exception as e:
        print("mail service send token error", e)
        time.sleep(1)
