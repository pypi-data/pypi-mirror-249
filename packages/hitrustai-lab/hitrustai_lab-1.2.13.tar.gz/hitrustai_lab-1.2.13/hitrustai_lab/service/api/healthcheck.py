import requests
from datetime import datetime
from healthcheck import HealthCheck

from ..api import encrypt_token


class DataPayload:
    Payloads = {
        'card-abnormal': {
            "diia_serial_number": "test_diia_serial_number",
            "connector_id": "test_connector_id",
            "institute_id": "test_institute_id",
            "operator_id": "test_operator_id",
            "serial_number": "unittestSN12345786789",
            "customer_servertime": "2021-11-09 05:10:10",
            "pan_hash": "unit_test_card_0",
            "merchant_id": "23456",
            "purchase_amount": "2013000",
            "purchase_currency": "901",
            "udid": "unit_test_udid_0",
            "ip_country": "Taiwan",
            "os_name": "Windows",
            "browser_language": "zh-TW",
            "ip_request": "192.168.100.203"
        },
        'card-testing': {
            "diia_serial_number": "test_diia_serial_number",
            "institute_id": "I999",
            "operator_id": "O001",
            "connector_id": "8909191002",
            "serial_number": "unittestSN12345786789",
            "udid": "1234567890123456789",
            "customer_servertime": "2021-11-20 12:59:56",
            "pan_hash": "34m4MOQAZM9/BQVpSimvaLjeYgBUxqBi6zr4SGLqg9QbJ1D82zQxtvu4YnoyA==1",
            "pan_expire": "2032",
            "merchant_id": "451615MID001",
            "card_bin": "101671****6012",
            "ip_request": "201.167.110.111",
            "ip_source": "201.167.117.111"
        },
        'fraud-detect': {
            'udid': '1516109167423655936',
            'serial_number': 'daa07c27302eb4eb5aa05e93b63b812a159e651frJhNcdcf1n74TwAS',
            'diia_serial_number': 'c695f0aae9e528f22a38e201d2a9c8e5',
            'connector_id': 'AI_CONNECTOR',
            'operator_id': 'SYSOPERATOR',
            'institute_id': '2020',
            'client_account': 'admin',
            'hardware_device_type': 'Desktop or Laptop',
            'hardware_device_model': 'Macintosh',
            'hardware_device_brand': 'Apple',
            'hardware_pointing_method': 'Mouse',
            'hardware_gpu_name': 'Intel(R) Iris(TM) Graphics 6100',
            'hardware_cpu_architecture': 'x86-64',
            'os_name': 'macOS',
            'os_platform': 'MacIntel',
            'os_screen_color_depth': '30-bit',
            'os_screen_pixel_ratio': '2',
            'os_screen_resolution_width': '1440',
            'os_screen_resolution_height': '764',
            'os_screen_orientation': 'Landscape',
            'os_local_timezone_offset': '+8',
            'os_local_datetime': 'Mon Nov 22 2021 18:12:00 GMT+0800 (Taipei Standard Time)',
            'os_local_timezone': 'Asia/Taipei',
            'browser_name': 'Safari Browser',
            'browser_engine': 'Webkit',
            'browser_is_tor': 'False',
            'browser_is_brave': 'False',
            'browser_resolution_width': '1440',
            'browser_resolution_height': '764',
            'browser_is_private_mode': 'False',
            'browser_is_use_adblock': 'True',
            'browser_language': 'en',
            'browser_account_login': 'undefined',
            'browser_useragent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'browser_req_useragent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
            'ip_is_proxy': 'False',
            'ip_is_tor': 'False',
            'ip_is_vpn': 'False',
            'ip_country': 'Taiwan',
            'ip_cloud_server': 'False',
            'ip_timezone': 'Asia/Taipei',
            'ip_source': '59.125.100.235',
            'ip_request': '59.125.100.235',
            'ip_isp': 'HiNet',
            'robot': {
                'serial_number': 'wnj31g38qn07u332gwpz8jmxg49zooha7gyfk3w1',
                'client_account': 'admin',
                'platform': 'MacIntel',
                'vendor': 'Google Inc.',
                'renderer': 'Google SwiftShader',
                'useragent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
                'webdriver': '0',
                'is_private_mode': 'False',
                'eval': 33,
                'mouse_enter': '1',
                'mouse_click': '1',
                'touch_start': '0',
                'tab': '0',
                'paste': '0',
                'is_change_useragent': 'False',
                'is_change_plugins': 'False',
                'is_change_languages': 'False',
                'is_change_webdriver': 'False',
                'is_change_eval': 'False',
                'is_change_platform': 'False',
                'page_time': 10.646,
                'mouse_log': '[{"pageX":439,"pageY":402,"count":1,"timeStamp":"2220.800"},{"pageX":660,"pageY":450,"count":14,"timeStamp":"5034.100"},{"pageX":490,"pageY":714,"count":1,"timeStamp":"5132.300"},{"pageX":466,"pageY":733,"count":1,"timeStamp":"5230.800"},{"pageX":428,"pageY":743,"count":1,"timeStamp":"5329.100"},{"pageX":365,"pageY":735,"count":1,"timeStamp":"5435.700"},{"pageX":327,"pageY":691,"count":1,"timeStamp":"5534.400"},{"pageX":320,"pageY":683,"count":1,"timeStamp":"5624.600"},{"pageX":319,"pageY":682,"count":1,"timeStamp":"5731.100"}]',
                'events_log': '[{"event":"mouseenter","time":1655271109666,"pageX":439,"pageY":402,"name":"inputUsername","input_order":"inputOrder1","timeStamp":2138.5},{"event":"click","time":1655271110179,"pageX":439,"pageY":402,"name":"inputUsername","input_order":"inputOrder1","timeStamp":2645.6}]',
                'resolution_width': '1440',
                'resolution_height': '900',
                'pixel_ratio': '1',
                'source_ip': '102.125.100.235',
                'CreateTime': '2022-06-15T05:31:53.8637Z'
            },
            'deviceinfo_create_time': '2021-11-17 09:50:06'
        },
        'account-takeover': {
            'serial_number': 'test1',
            'diia_serial_number': '123',
            'connector_id': '123',
            'institute_id': '11001',
            'operator_id': '123',
            'account': {'account': 'test11@gmail.com'},
            'device': {
                'udid': '14421239600917281',
                'hardware_device_type': 'Desktop or Laptop',
                'os_name': 'macOS',
                'os_version': '10.15.7'
            },
            'ip': {
                'ip_request': '1250.117.43.39',
                'ip_latitude': '253.0127',
                'ip_longitude': '1121.4609',
                'ip_is_proxy': 'False',
                'ip_is_vpn': 'False',
                'ip_is_tor': 'False',
                'ip_cloud_server': 'False'
            }
        },
        'merchant-risk': {
            'serial_number': 'test',
            'diia_serial_number': '123',
            'connector_id': '123',
            'institute_id': '123',
            'operator_id': '123',
            'client_account': 'admin',
            'merchant_id': 'merchant_3',
            'pan_hash': 'c1014',
            'purchase_amount': 35000000,
            'purchase_currency': 'TWD',
            'merchatrisk_create_time': '2022-08-15 10:10:10'
        },
        'gateway-acqfd': {
            'cifNumber': None,
            'cardScheme': 'M',
            'processType': '01',
            'txInfo': {
                'threeDSRequestorAuthenticationInd': None,
                'threeDSRequestorAuthenticationInfo': {
                    'threeDSReqAuthData': '111',
                    'threeDSReqAuthMethod': None,
                    'threeDSReqAuthTimestamp': None
                },
                'acctType': '01',
                'acquirerBIN': '1231234',
                'acquirerMerchantId': '8909191',
                'addrMatch': None,
                'acctInfo': {
                    'chAccAgeInd': '01',
                    'chAccChange': None,
                    'chAccChangeInd': None,
                    'chAccDate': None,
                    'chAccPwChange': None,
                    'chAccPwChangeInd': None,
                    'nbPurchaseAccount': None,
                    'provisionAttemptsDay': None,
                    'txnActivityDay': None,
                    'txnActivityYear': None,
                    'paymentAccAge': None,
                    'paymentAccInd': None,
                    'shipAddressUsage': None,
                    'shipAddressUsageInd': None,
                    'shipNameIndicator': None,
                    'suspiciousAccActivity': None
                },
                'cardNo': None,
                'cardBin': None,
                'acctID': 'F123456789',
                'transType': None,
                'billAddrCity': None,
                'billAddrCountry': None,
                'billAddrLine1': None,
                'billAddrLine2': None,
                'billAddrLine3': None,
                'billAddrPostCode': None,
                'billAddrState': None,
                'email': None,
                'emailMask': None,
                'homePhone': None,
                'mobilePhone': None,
                'workPhone': None,
                'cardholderName': None,
                'cardExpiryDate': '2512',
                'shipAddrCity': None,
                'shipAddrCountry': None,
                'shipAddrLine1': None,
                'shipAddrLine2': None,
                'shipAddrLine3': None,
                'shipAddrPostCode': None,
                'shipAddrState': None,
                'deviceChannel': '03',
                'purchaseInstalData': None,
                'mcc': None,
                'merchantCountryCode': None,
                'merchantName': None,
                'merchantRiskIndicator': None,
                'messageCategory': '01',
                'purchaseAmount': '99900',
                'purchaseCurrency': '901',
                'purchaseExponent': '2',
                'purchaseDate': None,
                'recurringExpiry': None,
                'recurringFrequency': None,
                'whiteListStatus': None,
                'whiteListStatusSource': None,
                'threeDSRequestorPriorAuthenticationInfo': None,
                'cardholderInfo': None,
                'threeRIInd': None,
                'threeDSRequestorDecMaxTime': None,
                'threeDSRequestorDecReqInd': None,
                'threeDSCompInd': None,
                'threeDSReqAuthMethodInd': None,
                'threeDSRequestorChallengeInd': None,
                'threeDSRequestorID': None,
                'threeDSRequestorName': None,
                'threeDSServerRefNumber': None,
                'browserAcceptHeader': None,
                'browserIP': None,
                'browserJavaEnabled': None,
                'browserJavascriptEnabled': None,
                'browserLanguage': None,
                'browserColorDepth': None,
                'browserScreenHeight': None,
                'browserScreenWidth': None,
                'browserTZ': None,
                'browserUserAgent': None,
                'messageExtension': None,
                'acctNumber': 'xxxxxxxxxxxxxxx',
                'acctNumberMask': '353352******0123',
                'cifNumber': None,
                'payTokenInd': None,
                'payTokenSource': None,
                'messageVersion': None,
                'sdkAppID': None,
                'sdkMaxTimeout': None,
                'threeDSServerTransID': None,
                'dsTransID': None,
                'sdkReferenceNumber': None,
                'realAmount': None,
                'realAmountInUsd': None,
                'mcScore': None,
                'mcDecision': None,
                'mcReasonCode1': None,
                'mcReasonCode2': None
            },
            'diiaInfo': {
                'deviceInfo': None,
                'robotInfo': None,
                'serialNumber': 'sn0000000011',
                'diiaSerialNumber': 'b49448532cd2037af4291f4e8b141a49'
            },
            'ak': None,
            'mode': '1',
            'promoteInfo': None,
            'operatorId': 'HT158001',
            'instituteId': 'acqfdtest',
            'merchantId': None,
            'connectorId': 'IB_TW007_TEST_1',
            'version': '2.0.0',
            'veriIdTransID': 'a17f9339-bafa-456a-917b-4deeb553f955',
            'mac': 'PSf+JCK98+T7wEKo59AupSifzt1gqx+Yuu2y4xv2gFbVB1gmVjBovvEEtPM7T4/0Mc96Kb8uCFEc0uIqOEolXg==',
            'timestamp': '20230309062402',
            'clientTransId': '5681830f-a645-4b20-84be-cf6e3c0f3799'
        },
        'gateway-ibfd': {
            'diia_serial_number': '27e2727bdd52dfdd9f99cab95bdbce07',
            'serial_number': 'TEST-b52aee47514309ce9bfb678d5d56b738bb1a8d5336ETV2LCK5EFJUSN1',
            'loginType': 'account',
            'loginSuccess': 'Y',
            'accountId': 'user02',
            'operatorId': 'HT158001',
            'instituteId': 'ibfdtest',
            'connectorId': 'IB_TW007_TEST_1',
            'version': '2.0.0',
            'mac': 'Q9qmvMsmEKFmh3oJKbAddkcugqP69PuiKgHt4Sa1ff76DGJnnigdXZQADaK+hvXfpi+WmCJ4YHSBaz4M8PH1mg==',
            'timestamp': '1652171287345',
            'firstStepSuccess': 'Y',
            'isStepUp': 'Y'
        },
        'gateway-isrfd': {
            'cifNumber': None,
            'cardScheme': 'V',
            'processType': None,
            'txInfo': {
                'threeDSRequestorAuthenticationInd': '01',
                'threeDSRequestorAuthenticationInfo': {
                    'threeDSReqAuthData': None,
                    'threeDSReqAuthMethod': None,
                    'threeDSReqAuthTimestamp': None
                },
                'acctType': '01',
                'acquirerBIN': '1231234',
                'acquirerMerchantId': '8909191',
                'addrMatch': None,
                'acctInfo': {
                    'chAccAgeInd': '',
                    'chAccChange': '',
                    'chAccChangeInd': '',
                    'chAccDate': '',
                    'chAccPwChange': '',
                    'chAccPwChangeInd': '',
                    'nbPurchaseAccount': '',
                    'provisionAttemptsDay': '',
                    'txnActivityDay': '',
                    'txnActivityYear': '',
                    'paymentAccAge': '',
                    'paymentAccInd': '',
                    'shipAddressUsage': '',
                    'shipAddressUsageInd': '',
                    'shipNameIndicator': '',
                    'suspiciousAccActivity': ''
                },
                'cardNo': None,
                'cardBin': 'demo',
                'acctID': 'Q9X0hNlhnPh8+gA4TVZScqeOO6txgIGjDMSIYcCiunfaYq48F7ee/FmNBPSBtdhaZ1i5xU7d7z7TX5NEqnDSfg==',
                'transType': None,
                'billAddrCity': '',
                'billAddrCountry': '',
                'billAddrLine1': '',
                'billAddrLine2': '',
                'billAddrLine3': '',
                'billAddrPostCode': '',
                'billAddrState': '',
                'email': '',
                'emailMask': '',
                'homePhone': {'cc': '', 'subscriber': '', 'subscriberMask': None},
                'mobilePhone': {'cc': '', 'subscriber': '', 'subscriberMask': None},
                'workPhone': {'cc': '', 'subscriber': '', 'subscriberMask': None},
                'cardholderName': '',
                'cardExpiryDate': '2512',
                'shipAddrCity': '',
                'shipAddrCountry': '',
                'shipAddrLine1': '',
                'shipAddrLine2': '',
                'shipAddrLine3': '',
                'shipAddrPostCode': '',
                'shipAddrState': '',
                'deviceChannel': '02',
                'purchaseInstalData': None,
                'mcc': '5661',
                'merchantCountryCode': '158',
                'merchantName': 'HiTRUST ACQFD Merchant Simulator',
                'merchantRiskIndicator': {
                    'deliveryEmailAddress': '',
                    'deliveryTimeframe': '',
                    'giftCardAmount': '',
                    'giftCardCount': '',
                    'giftCardCurr': '',
                    'preOrderDate': '',
                    'preOrderPurchaseInd': '',
                    'reorderItemsInd': '',
                    'shipIndicator': ''
                },
                'messageCategory': '01',
                'purchaseAmount': '100',
                'purchaseCurrency': '901',
                'purchaseExponent': '2',
                'purchaseDate': '20230912065656',
                'recurringExpiry': '',
                'recurringFrequency': '',
                'whiteListStatus': None,
                'whiteListStatusSource': None,
                'threeDSRequestorPriorAuthenticationInfo': None,
                'cardholderInfo': None,
                'threeRIInd': None,
                'threeDSRequestorDecMaxTime': None,
                'threeDSRequestorDecReqInd': None,
                'threeDSCompInd': 'Y',
                'threeDSReqAuthMethodInd': None,
                'threeDSRequestorChallengeInd': None,
                'threeDSRequestorID': '12128301823081230123',
                'threeDSRequestorName': 'demo',
                'threeDSServerRefNumber': 'demo',
                'browserAcceptHeader': 'demo',
                'browserIP': None,
                'browserJavaEnabled': 'false',
                'browserJavascriptEnabled': 'false',
                'browserLanguage': 'demo',
                'browserColorDepth': 'demo',
                'browserScreenHeight': 'demo',
                'browserScreenWidth': 'demo',
                'browserTZ': None,
                'browserUserAgent': 'demo',
                'messageExtension': None,
                'acctNumber': 'y74bWBsLzBv2Kw2dfRTE3mg8zm4w1Go7nYVpNV1Zjmg/UoepjHTlTq1srdwnrak5GV+w0RulMVtoxotUupS7Ew==',
                'acctNumberMask': '51535200****0123',
                'cifNumber': None,
                'payTokenInd': None,
                'payTokenSource': None,
                'messageVersion': 'demo',
                'sdkAppID': None,
                'sdkMaxTimeout': None,
                'threeDSServerTransID': None,
                'dsTransID': None,
                'sdkReferenceNumber': None,
                'realAmount': None,
                'realAmountInUsd': None,
                'mcScore': None,
                'mcDecision': None,
                'mcReasonCode1': None,
                'mcReasonCode2': None
            },
            'diiaInfo': {
                'deviceInfo': 'eyJzZXJpYWxfbnVtYmVyIjoidGVzdFpqRXdPV1ExTURndFl6ZG1NeTAwWm1Vd0xXRmpaRFF0T0RFM056bGxNakpsWWpNMyIsImRpaWFfc2VyaWFsX251bWJlciI6ImI5YTgzNzA4ZmVmMTA4NzBkMGM1OTczOTgxMzg3Mjk4IiwiY2xpZW50X2FjY291bnQiOiJJU1JfVFcwMDhfVEVTVF8xLTE0MSIsInVkaWQiOiJVMTY4MzcxNjY5NjgzMDkwNjM2OCIsImhhcmR3YXJlX2RldmljZV90eXBlIjoiRGVza3RvcCBvciBMYXB0b3AiLCJoYXJkd2FyZV9kZXZpY2VfbW9kZWwiOiJuYW4iLCJoYXJkd2FyZV9kZXZpY2VfYnJhbmQiOiJuYW4iLCJoYXJkd2FyZV9jcHVfYXJjaGl0ZWN0dXJlIjoieDg2LTY0IiwiaGFyZHdhcmVfY3B1X2NvcmVzIjoiOCIsImhhcmR3YXJlX21lbW9yeV9zaXplIjoiOCBHQiBvciBtb3JlIiwiaGFyZHdhcmVfZ3B1X25hbWUiOiJBTkdMRSAoSW50ZWwsIEludGVsKFIpIFVIRCBHcmFwaGljcyA2MjAgRGlyZWN0M0QxMSB2c181XzAgcHNfNV8wLCBEM0QxMSkiLCJoYXJkd2FyZV9pc19iYXR0ZXJ5X2NoYXJnaW5nIjoiVHJ1ZSIsImhhcmR3YXJlX2JhdHRlcnlfbGV2ZWwiOiIxMDAlIiwiaGFyZHdhcmVfYXVkaW9fZnAiOiIxZGExNjg4YzllNDk2OGZlMzBiMTQ0NzhlZmZlOGZhYyIsImhhcmR3YXJlX3BvaW50aW5nX21ldGhvZCI6Ik1vdXNlIiwiaGFyZHdhcmVfbWF4X3RvdWNoX3BvaW50cyI6IjAiLCJvc19uYW1lIjoiV2luZG93cyIsIm9zX3ZlcnNpb24iOiIxMC4wIiwib3NfcGxhdGZvcm0iOiJXaW4zMiIsIm9zX2xvY2FsX2RhdGV0aW1lIjoidGlueSBtb2RlIiwib3NfbG9jYWxfdGltZXpvbmUiOiJBc2lhL1RhaXBlaSIsIm9zX2xvY2FsX3RpbWV6b25lX29mZnNldCI6Iis4Iiwib3Nfc2NyZWVuX29yaWVudGF0aW9uIjoiTGFuZHNjYXBlIiwib3Nfc2NyZWVuX3Jlc29sdXRpb25fd2lkdGgiOiIxOTIwIiwib3Nfc2NyZWVuX3Jlc29sdXRpb25faGVpZ2h0IjoiMTA4MCIsIm9zX3NjcmVlbl9waXhlbF9yYXRpbyI6IjAuODk5OTk5OTc2MTU4MTQyMSIsIm9zX3NjcmVlbl9jb2xvcl9kZXB0aCI6IjI0LWJpdCIsImlwX3NvdXJjZSI6IjU5LjEyNS4xMDAuMjM3IiwiaXBfZm91bmRhdGlvbiI6ImYtMTU5MjIyMDY5MyIsImlwX2ludHJhbmV0IjoidGlueSBtb2RlIiwiaXBfc3JjX2xhdGl0dWRlIjoiMjUuMDQ3OCIsImlwX3NyY19sb25naXR1ZGUiOiIxMjEuNTMxOCIsImlwX3NyY190aW1lem9uZSI6IkFzaWEvVGFpcGVpIiwiaXBfc3JjX2NvdW50cnkiOiJUYWl3YW4iLCJpcF9yZXF1ZXN0IjoiNTkuMTI1LjEwMC4yMzciLCJpcF9sYXRpdHVkZSI6IjI1LjA0NzgiLCJpcF9sb25naXR1ZGUiOiIxMjEuNTMxOCIsImlwX3RpbWV6b25lIjoiQXNpYS9UYWlwZWkiLCJpcF9jb3VudHJ5IjoiVGFpd2FuIiwiaXBfaXNwIjoiSGlOZXQiLCJpcF9ob3N0bmFtZSI6Im5hbiIsImlwX2lzX3Byb3h5IjoiRmFsc2UiLCJpcF9pc190b3IiOiJGYWxzZSIsImlwX2lzX3ZwbiI6IkZhbHNlIiwiaXBfY2xvdWRfc2VydmVyIjoiRmFsc2UiLCJicm93c2VyX25hbWUiOiJDaHJvbWUgQnJvd3NlciIsImJyb3dzZXJfdmVyc2lvbiI6IjExNi4wLjAuMCIsImJyb3dzZXJfZW5naW5lIjoiQmxpbmsiLCJicm93c2VyX3Jlc29sdXRpb25fd2lkdGgiOiIyMTMzIiwiYnJvd3Nlcl9yZXNvbHV0aW9uX2hlaWdodCI6IjEwMzQiLCJicm93c2VyX3VybCI6Imh0dHBzOi8vYXBpLnZlcmktaWQtdWF0LmNvbS9hY3FmZC1kZW1vLXdlYi9pc3JmZF9wIiwiYnJvd3Nlcl91c2VyYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTE2LjAuMC4wIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3JlcV91c2VyYWdlbnQiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvMTE2LjAuMC4wIFNhZmFyaS81MzcuMzYiLCJicm93c2VyX3BsdWdpbnMiOiJ0aW55IG1vZGUiLCJicm93c2VyX21pbWV0eXBlcyI6InRpbnkgbW9kZSIsImJyb3dzZXJfbGFuZ3VhZ2UiOiJ6aC1UVyIsImJyb3dzZXJfbGFuZ3VhZ2VfZnAiOiJiMzI0MDJhZTQxMmJlN2YzY2FmYmRhZjEyYWM3ZjEwZCIsImJyb3dzZXJfaXNfc3VwcG9ydF9jYW52YXMiOiJUcnVlIiwiYnJvd3Nlcl9jYW52YXNfZnAiOiI4YzM2YjdlZTg4ZmVlMzlmNTBlMzIzZTgyZTFhNmEzYiIsImJyb3dzZXJfbnVtYmVyX29mX2F2YWlsYWJsZV9mb250cyI6IjQ4IC8gNjQiLCJicm93c2VyX2F2YWlsYWJsZV9mb250cyI6InRpbnkgbW9kZSIsImJyb3dzZXJfZm9udHNfZnAiOiI4MmI2MmQxYSIsImJyb3dzZXJfaXNfc3VwcG9ydF93ZWJnbDEiOiJUcnVlIiwiYnJvd3Nlcl9pc19zdXBwb3J0X3dlYmdsMiI6IlRydWUiLCJicm93c2VyX3dlYmdsX2ZwIjoiODViYzY4ZWU4YjY4OGE0YmU1NmE5Zjk0YzM1NGY4ZTQiLCJicm93c2VyX2lzX3N1cHBvcnRfY29va2llcyI6IlRydWUiLCJicm93c2VyX2lzX3N1cHBvcnRfd2VicnRjIjoiVHJ1ZSIsImJyb3dzZXJfaXNfc3VwcG9ydF93ZWJzb2NrZXQiOiJUcnVlIiwiYnJvd3Nlcl9pc19zdXBwb3J0X2luZGV4ZWRkYiI6IlRydWUiLCJicm93c2VyX2lzX3N1cHBvcnRfbG9jYWxfc3RvcmFnZSI6IlRydWUiLCJicm93c2VyX2lzX3N1cHBvcnRfc2Vzc2lvbl9zdG9yYWdlIjoiVHJ1ZSIsImJyb3dzZXJfaXNfc3VwcG9ydF9vcGVuX2RhdGFiYXNlIjoiVHJ1ZSIsImJyb3dzZXJfaHR0cF92ZXJzaW9uIjoiSFRUUC8xLjEiLCJicm93c2VyX2FjY2VwdGVkX2NvbnRlbnRfZW5jb2RpbmdzIjoiZ3ppcCwgZGVmbGF0ZSwgYnIiLCJicm93c2VyX2lzX3ByaXZhdGVfbW9kZSI6IkZhbHNlIiwiYnJvd3Nlcl9pc191c2Vfd2ViZHJpdmVyIjoiRmFsc2UiLCJicm93c2VyX2lzX2JyYXZlIjoiRmFsc2UiLCJicm93c2VyX2lzX3RvciI6IkZhbHNlIiwiZ2V0X3ZlcnNpb24iOiJ2NCIsImZpcnN0X3NlZW4iOiIyMDIzLTA3LTI1IDA1OjUxOjU4IiwibGFzdF91cGRhdGUiOiIyMDIzLTA5LTEyIDA2OjU2OjU0IiwiZGV2aWNlaW5mb19jcmVhdGVfdGltZSI6IjIwMjMtMDktMTIgMDY6NTY6NTQiLCJzdGF0dXMiOiI0MDAxIn0=',
                'robotInfo': {
                    'serial_number': 'testZjEwOWQ1MDgtYzdmMy00ZmUwLWFjZDQtODE3NzllMjJlYjM3',
                    'diia_serial_number': 'b9a83708fef10870d0c5973981387298',
                    'client_account': 'ISR_TW008_TEST_1-141',
                    'platform': 'Win32',
                    'vendor': 'Google Inc. (Intel)',
                    'renderer': 'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)',
                    'webdriver': '0',
                    'is_private_mode': 'False',
                    'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
                    'eval': 33,
                    'is_change_useragent': 'False',
                    'is_change_plugins': 'False',
                    'is_change_languages': 'False',
                    'is_change_webdriver': 'False',
                    'is_change_eval': 'False',
                    'is_change_platform': 'False',
                    'mouse_enter': '1',
                    'mouse_click': '0',
                    'touch_start': '0',
                    'paste': '0',
                    'tab': '0',
                    'page_time': 2.504,
                    'mouse_log': '[{"pageX":1207,"pageY":368,"count":1,"timeStamp":"806.600"},{"pageX":1225,"pageY":374,"count":1,"timeStamp":"847.300"},{"pageX":1228,"pageY":374,"count":1,"timeStamp":"967.300"},{"pageX":1236,"pageY":373,"count":6,"timeStamp":"1607.500"},{"pageX":1240,"pageY":372,"count":1,"timeStamp":"1623.600"},{"pageX":1241,"pageY":372,"count":2,"timeStamp":"1912.200"},{"pageX":1043,"pageY":753,"count":1,"timeStamp":"2006.600"},{"pageX":884,"pageY":936,"count":1,"timeStamp":"2103.700"},{"pageX":836,"pageY":916,"count":1,"timeStamp":"2207.200"},{"pageX":758,"pageY":892,"count":1,"timeStamp":"2305.300"},{"pageX":745,"pageY":894,"count":1,"timeStamp":"2342.200"}]',
                    'events_log': '[{"event":"mouseenter","time":1694501850884,"pageX":948,"pageY":362,"name":"txInfo.purchaseDate","input_order":"inputOrder3","timeStamp":717.8}]',
                    'resolution_width': '1920',
                    'resolution_height': '1080',
                    'pixel_ratio': '0.8999999761581421',
                    'source_ip': '59.125.100.237'
                },
                'serialNumber': 'testZjEwOWQ1MDgtYzdmMy00ZmUwLWFjZDQtODE3NzllMjJlYjM3',
                'diiaSerialNumber': 'b9a83708fef10870d0c5973981387298'
            },
            'operatorId': 'BA036001',
            'instituteId': '11003',
            'merchantId': None,
            'connectorId': 'ISR_AU001_BANO_1',
            'version': '1.0.0',
            'mac': 'nRwtlNRj9FbvYmFcNg9M107nOkXvy8xM+hDkxRgX4GssGNKyySnTJ8XxUGVF7thSd08IbE+qMxcYiRSzt51uyQ==',
            'timestamp': '20230912065656',
            'clientTransId': 'f109d508-c7f3-4fe0-acd4-81779e22eb37'
        }
    }

    def add_payload(self, model_name: str, payload: dict):
        self.Payloads.update({model_name: payload})

    def get(self, model_name: str, token: str, timestamp: str):
        if model_name not in self.Payloads:
            return {}

        now = datetime.now()
        payload = self.Payloads.get(model_name)

        if 'gateway' in model_name:
            return payload

        payload.update({
            "diia_serial_number": f"TEST-{now}",
            "serial_number": f"TEST-{now}",
        })
        return {
            "data_version": "1.0.0",
            "mac": encrypt_token(token, timestamp),
            "timestamp": timestamp,
            "payload": payload
        }


class Healthchecker(DataPayload):
    def __init__(self, model_name: str, token: str, timestamp: str, update_pan_hash=True, domain='http://127.0.0.1:8080'):
        self.model_name = model_name
        self.TOKEN = token
        self.TIMESTAMP = timestamp
        self.UpdatePanHash = update_pan_hash
        self.domain = domain

    def post_v2(self):
        url = f"{self.domain}/model/predict/{self.model_name}/v2/api/predict"
        input_data = self.get(
            self.model_name, self.TOKEN, timestamp=self.TIMESTAMP)

        if (
            ('payload' in input_data) and
            ('pan_hash' in input_data['payload']) and
            self.UpdatePanHash
        ):
            now = datetime.now()
            input_data['payload']['pan_hash'] = f"unit_test_card_{now}"

        contents = requests.post(url, json=input_data)
        if contents.status_code == 200:
            output = contents.json()
            if output['return_code'] == "4003":
                return True, "4003"
            return False, output["return_code"]
        return False, str(contents.status_code)

    @staticmethod
    def add_healthcheck_url(app, check_func, url: str):
        health_check = HealthCheck()
        health_check.add_check(check_func)
        app.add_url_rule(url, "healthcheck",
                         view_func=lambda: health_check.run())
        return app
