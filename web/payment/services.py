# services.py
import requests

class SampleService:
    def ready(self, agent, open_type):
        url = "https://kapi.kakao.com/v1/payment/ready"
        headers = {
            "Authorization": "KakaoAK fe83a8063428f1aaa8bde37f101ec1a4",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        data = {
            # data to be sent with the request
            "cid": "TC0ONETIME",
            # partner_order_id
            "partner_order_id": "1",
            # partner_user_id
            "partner_user_id": "5",
            "item_name": "초코파이",
            "quantity": "1",
            "total_amount": "2200",
            "vat_amount": "200",
            "tax_free_amount": "0",
            "approval_url": "https://developers.kakao.com/success",
            "fail_url": "https://developers.kakao.com/fail",
            "cancel_url": "https://developers.kakao.com/cancel"
        }
        response = requests.post(url, headers=headers, data=data)
        return response.json()

    def approve(self, pg_token):
        url = "https://kapi.kakao.com/v1/payment/approve"
        headers = {
            "Authorization": "KakaoAK fe83a8063428f1aaa8bde37f101ec1a4",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        data = {
            # data to be sent with the request
        }
        response = requests.post(url, headers=headers, data=data)
        return response.json()
