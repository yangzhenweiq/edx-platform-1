from .devstack_docker import *

FEATURES.update({
    'ENABLE_MEMBERSHIP_INTEGRATION': True,
    'ENABLE_PAYMENTS_INTEGRATION': True,
    'ENABLE_PROFESSORS': True,
})

# Payment
ALIPAY_INFO = AUTH_TOKENS.get('ALIPAY_INFO', ALIPAY_INFO)
ALIPAY_APP_INFO = AUTH_TOKENS.get('ALIPAY_APP_INFO', ALIPAY_APP_INFO)
WECHAT_PAY_INFO = AUTH_TOKENS.get('WECHAT_PAY_INFO', WECHAT_PAY_INFO)
WECHAT_APP_PAY_INFO = AUTH_TOKENS.get('WECHAT_APP_PAY_INFO', WECHAT_APP_PAY_INFO)
WECHAT_H5_PAY_INFO = AUTH_TOKENS.get('WECHAT_H5_PAY_INFO', WECHAT_H5_PAY_INFO)
# Aliyun oss
ALIYUN_OSS = AUTH_TOKENS.get('ALIYUN_OSS', {})

OSS_ACCESS_KEY_ID = ALIYUN_OSS.get("OSS_ACCESS_KEY_ID", "")
OSS_ACCESS_KEY_SECRET = ALIYUN_OSS.get("OSS_ACCESS_KEY_SECRET", "")
OSS_ENDPOINT = ALIYUN_OSS.get("OSS_ENDPOINT", "")
OSS_BUCKET_NAME = ALIYUN_OSS.get("OSS_BUCKET_NAME", "")

# for SMS
SMS_API = AUTH_TOKENS.get('SMS_API', '')
SMS_API_BY_LINKGROUP = AUTH_TOKENS.get('SMS_API_BY_LINKGROUP', '')
SMS_API_URL = ENV_TOKENS.get('SMS_API_URL', '')
SMS_API_URL_BY_LINKGROUP = ENV_TOKENS.get('SMS_API_URL_BY_LINKGROUP', '')

if FEATURES.get('ENABLE_MEMBERSHIP_INTEGRATION', False):
    INSTALLED_APPS.append('membership')
    REST_FRAMEWORK.update({'EXCEPTION_HANDLER': 'membership.utils.customer_exception_handler'})

######################## Professors ###########################
if FEATURES.get('ENABLE_PROFESSORS'):
    INSTALLED_APPS.append('professors')

############################ WEIXINAPPID_AND_WEIXINAPPSECRET #########################
WEIXINAPPID = ''
WEIXINAPPSECRET = ''
WEIXINAPPID = ENV_TOKENS.get('WEIXINAPPID', WEIXINAPPID)
WEIXINAPPSECRET = ENV_TOKENS.get('WEIXINAPPSECRET', WEIXINAPPSECRET)
