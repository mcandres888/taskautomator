import os, sys
import requests
import json

# get config data
# load library path
lib_path = os.path.abspath(os.path.join(".."))
sys.path.append(lib_path)

from config import *

CONFIG = DevelopmentConfig()

print CONFIG.API_URL
data = {
  "_id": "4d5b3624fe7e4e6aace8277bac008bc4",
  "_rev": "1-0a4ab07b36af092dc301c9a469e0cfb2",
  "P5_discount": 0,
  "cancelled_items": [],
  "updated_at": "",
  "item_discount": 0,
  "cashier_id": "f026b805-e720-3cb9-7d91-824619278964",
  "deleted_at": "",
  "total_items": 4,
  "senior_discount": 0,
  "total_cancelled_amount": 0,
  "pwd_discount": 0,
  "printer_status": "not printed",
  "receipt_no": "000-000000000016",
  "type": "vend",
  "vat": 35.35714285714285,
  "status": "processed",
  "card_name": "",
  "excess_gc": 0,
  "vatable": 294.6428571428571,
  "P20_discount": 0,
  "less_vat": 0,
  "cashier": "John  Doe",
  "change_amount": 0,
  "customer_name": "Marc Andres",
  "customer_email": "",
  "customer_barcode": "",
  "discount": 0,
  "vat_exempt": 0,
  "loyalty_point": 0,
  "mode_of_payment": {
    "bank_cheque": {
      "cheque_no": "",
      "bank_name": "",
      "amount": 0,
      "is_active": "false"
    },
    "gift_cheque": {
      "ref_no": "",
      "amount": 0,
      "is_active": "false"
    },
    "cash": {
      "amount": 330,
      "is_active": "true"
    },
    "card": {
      "ref_no": "",
      "amount": 0,
      "is_active": "false"
    }
  },
  "date": "2020-01-13",
  "subtotal": 330,
  "device_id": "N/A",
  "price_net_of_vat": 0,
  "grand_total": 330,
  "items": [
    {
      "vat_exempt_per_srp": 0,
      "kilos": 0,
      "cost": 0,
      "pwd_discount_per_srp": 0,
      "unit": "pcs",
      "category": "Machine",
      "no": 1,
      "reg_discount_per_srp": 0,
      "itemcode": "11233",
      "return_number": "",
      "supplier": "Others",
      "is_zero_rated": "false",
      "senior_discount_per_piece": 0,
      "category2": "",
      "description": "WASHER SMALL MEDIUM WASH",
      "barcode": 123123123,
      "qty": 1,
      "subtotal": 80,
      "created_at": "2020-01-13 17:29:43",
      "void_number": "",
      "srp": 80,
      "total_amount_returns": 0,
      "machine_type": "washer",
      "machine_cycle": "medium",
      "machine_size": "small",
      "sc_type" : "30",
      "item_id": "4d5b3624fe7e4e6aace8277bac007f88"
    },
    {
      "vat_exempt_per_srp": 0,
      "kilos": 0,
      "cost": 0,
      "pwd_discount_per_srp": 0,
      "unit": "pcs",
      "category": "Machine",
      "no": 1,
      "reg_discount_per_srp": 0,
      "itemcode": "213123",
      "return_number": "",
      "supplier": "Others",
      "is_zero_rated": "false",
      "senior_discount_per_piece": 0,
      "category2": "",
      "description": "WASHER SMALL HEAVY WASH",
      "barcode": 21313123,
      "qty": 2,
      "subtotal": 180,
      "created_at": "2020-01-13 17:30:50",
      "void_number": "",
      "srp": 90,
      "total_amount_returns": 0,
      "machine_type": "washer",
      "machine_cycle": "heavy",
      "machine_size": "small",
      "sc_type" : "30",
      "item_id": "4d5b3624fe7e4e6aace8277bac008415"
    },
    {
      "vat_exempt_per_srp": 0,
      "kilos": 0,
      "cost": 0,
      "pwd_discount_per_srp": 0,
      "unit": "pcs",
      "category": "Machine",
      "no": 1,
      "reg_discount_per_srp": 0,
      "itemcode": "1212121",
      "return_number": "",
      "supplier": "Others",
      "is_zero_rated": "false",
      "senior_discount_per_piece": 0,
      "category2": "",
      "description": "WASHER SMALL LIGHT WASH",
      "barcode": 12121,
      "qty": 1,
      "subtotal": 70,
      "created_at": "2020-01-13 17:30:18",
      "void_number": "",
      "srp": 70,
      "total_amount_returns": 0,
      "machine_type": "washer",
      "machine_cycle": "light",
      "machine_size": "small",
      "sc_type" : "30",
      "item_id": "4d5b3624fe7e4e6aace8277bac0082c0"
    }
  ],
  "created_at": "2020-01-13 17:34:47",
  "cash_amount": 330,
  "transaction_object": {
    "transaction_no": 2,
    "transaction_count": 1
  },
  "zero_rated": 0,
  "action": "printable",
  "reg_discount": 0,
  "card_number": ""
}

print data

headers = {"Content-Type" : "Application/json"}

_url = "%s/customertransaction/add" % CONFIG.API_URL
res = requests.post(_url, data=json.dumps(data), headers=headers)
quit()








