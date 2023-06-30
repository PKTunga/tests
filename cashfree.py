import requests
import json

# endpoint = "https://sandbox.cashfree.com/pg/orders"
# appId = "2486760c0c523371555af3f992676842"
# secretKey = "4d285483b82e049c53a21452e537b08d4354095f"
# url = f"{endpoint}/orders"

# payload = json.dumps({
#   "customer_details": {
#     "customer_id": "7112AAA812234",
#     "customer_name": "name",
#     "customer_email": "johny@cashfree.com",
#     "customer_phone": "9908734801"
#   },
#   "order_meta": {
#     "notify_url": "https://webhook.site/0578a7fd-a0c0-4d47-956c-d02a061e36d3"
#   },
#   "order_amount": 1,
#   "order_id": "order_1626945143520",
#   "order_note": "Additional order info",
#   "order_currency": "INR"
# })
# headers = {
#   'Accept': 'application/json',
#   'x-api-version': '2022-01-01',
#   'Content-Type': 'application/json',
#   'x-client-id': f'{appId}',
#   'x-client-secret': f'{secretKey}'
# }

# response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)



# import requests
# import json

# url = "{{endpoint}}/orders/pay"

# payload = json.dumps({
#   "payment_method": {
#     "card": {
#       "card_number": "4160213000173499",
#       "card_holder_name": "Shubhi Maheshwari",
#       "card_expiry_mm": "04",
#       "card_expiry_yy": "27",
#       "card_cvv": "004",
#       "channel": "link"
#     }
#   },
#   "order_token": "3UVziw8AUKN8o5wWHm0a"
# })
# headers = {
#   'Content-Type': 'application/json',
#   'x-api-version': '{{version}}',
#   'Accept': 'application/json'
# }

# response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)







# import requests
# import json

# url = "{{endpoint}}/orders/pay"

# payload = json.dumps({
#   "payment_method": {
#     "upi": {
#       "upi_id": "success@upi",
#       "channel": "link"
#     }
#   },
#   "order_token": "HS4k8sStf2VLdggrxyfj"
# })
# headers = {
#   'Content-Type': 'application/json',
#   'x-api-version': '{{version}}',
#   'Accept': 'application/json'
# }

# response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)



# appId = "2486760c0c523371555af3f992676842"
# secretKey = "4d285483b82e049c53a21452e537b08d4354095f"



url = "https://api.cashfree.com/api/v1/order/create"

payload={
    'appId': '2486760c0c523371555af3f992676842',
    'secretKey': '955df43f13074bcafb77b52cee248687d4550943',
    'orderId': 'order_0011345266464422',
    'orderAmount': '1',
    'orderCurrency': 'INR',
    'orderNote': 'Test order',
    'customerEmail': 'sample@gmail.com',
    'customerName': 'Cashfree User',
    'customerPhone': '9999999999',
    'returnUrl': 'https://google.com',
    'notifyUrl': 'https://google.com',
}
files=[
]
headers = {}
response = requests.request("POST", url, data=payload)
print(response.text)
print(response.json())
paymentlink = response.json()["paymentLink"]
print(paymentlink)


# curl  --request POST --url https://sandbox.cashfree.com/pg/orders --header 'Content-Type: application/json' --header 'x-api-version: 2022-01-01' --header 'x-client-id: 2486760c0c523371555af3f992676842' --header 'x-client-secret: 4d285483b82e049c53a21452e537b08d4354095f' --data '{"order_id": "order_1626945143520","order_amount": 10.12,"order_currency": "INR","order_note": "Additional order info","customer_details": {"customer_id": "12345","customer_name": "name","customer_email": "care@cashfree.com","customer_phone": "9816512345"}}'