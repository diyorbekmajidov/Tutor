import requests
import random

def send_otp_tp_phone(phone_number):
    try:
        otp = random.randint(1000, 9999)
        url = "http://notify.eskiz.uz/api/message/sms/send"

        payload={'mobile_phone': phone_number,
        'message': otp,
        'from': '4546',
        'callback_url': 'http://0000.uz/test.php'}
        files=[

        ]
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTQ1NDQ0OTksImlhdCI6MTcxMTk1MjQ5OSwicm9sZSI6InVzZXIiLCJzaWduIjoiYTUzYzEzYzhhMzVlYzg1YWEyODAwMDJlZWNkNDZhZDdiMmU3ZmMxZTk0NWFmMjUwYjM3MjJlODQ5NTdkOWE1YiIsInN1YiI6IjI0NTkifQ.N50WBJwIfRvh8QiwDvmLFIdeXEHz63rtsiSjuanA_EM"
        headers = {'Authorization': "Bearer {}".format(token)}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        return otp
    except  Exception as e:
        return None
    
def send_sms_to_tutors_phone(phone_number, msg):
    try:
        url = "http://notify.eskiz.uz/api/message/sms/send"

        payload={'mobile_phone': phone_number,
        'message': msg,
        'from': '4546',
        'callback_url': 'http://0000.uz/test.php'}
        files=[

        ]
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTQ1NDQ0OTksImlhdCI6MTcxMTk1MjQ5OSwicm9sZSI6InVzZXIiLCJzaWduIjoiYTUzYzEzYzhhMzVlYzg1YWEyODAwMDJlZWNkNDZhZDdiMmU3ZmMxZTk0NWFmMjUwYjM3MjJlODQ5NTdkOWE1YiIsInN1YiI6IjI0NTkifQ.N50WBJwIfRvh8QiwDvmLFIdeXEHz63rtsiSjuanA_EM"
        headers = {'Authorization': "Bearer {}".format(token)}

        response = requests.request("POST", url, headers=headers, data=payload, files=files)
        return msg
    except  Exception as e:
        return None