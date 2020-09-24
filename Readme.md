```python
git clone https://github.com/shedolkar12/viandManagement.git

cd viandManagement

python3 -m venv venv
source venv/bin/activate

pip install djangorestframework
pip install Django==2.2

python manage.py makemigrations
python manage.py migrate

For adding sample data execute following command:
source add_sample_data.sh

Command for Local Server:
python manage.py runserver 8000


```
## Fetching combo Products API
```python
APIs:
GET: [http://localhost:8000/api/comboproducts/<branch_id>/]


sample request: [http://localhost:8000/api/comboproducts/123/]
<pre>
<code>
returns response:
{
  "offset": 0,
  "branch_id": 123,
  "combo_products": [
    {
      "description": "Seer(Vanjram/Surmai) Large 500gm, Prawns(500gm) and Rohu(Rui) Medium - Bengali Cut",
      "id": "prawns-seer_large-rohu_medium",
      "products": [
        {
          "unit": 0.5,
          "description": "Prawns",
          "id": "prawns",
          "price": 100
        },
        {
          "unit": 0.5,
          "description": "Seer(Vanjram/Surmai) Large",
          "id": "seer_large",
          "price": 500
        },
        {
          "unit": 0.5,
          "description": "Rohu(Rui) Medium - Bengali Cut",
          "id": "rohu_medium",
          "price": 300
        }
      ]
    },
    {
      "description": "Chicken Curry Cut Small(500gm) & Prawns",
      "id": "chicken_curry_cut_small-prawns",
      "products": [
        {
          "unit": 0.5,
          "description": "Chicken Curry Cut Small",
          "id": "chicken_curry_cut_small",
          "price": 120
        },
        {
          "unit": 0.5,
          "description": "Prawns",
          "id": "prawns",
          "price": 100
        }
      ]
    },
    {
      "description": "Chicken Curry Cut Small(500gm) and Biryani Cut(Goat)",
      "id": "chicken_curry_cut_small-biryani_goat_cut",
      "products": [
        {
          "unit": 0.5,
          "description": "Chicken Curry Cut Small",
          "id": "chicken_curry_cut_small",
          "price": 120
        },
        {
          "unit": 0.5,
          "description": "Biryani Cut(Goat)",
          "id": "biryani_goat_cut",
          "price": 500
        }
      ]
    }
  ],
  "limit": 10
}
-----------------------------------------------------------------------------
```
## API for Placing Order combo/individual products
```python
POST: http://127.0.0.1:8000/api/placeOrder/
request body:
{  
    "branch_id": 123, 
    "user_id": 34211, 
    "items": [
        {
            "type": "individual", 
            "products": [{"product_id": "chicken_curry_cut_small" }], 
            "quantity": 2
        },
        {
            "type": "combo", 
            "products": [{"product_id": "chicken_curry_cut_small" }, {"product_id": "prawns"}], 
            "quantity": 1
        }
        ], 
    "customer_address_id": 4542
}

...............................
Return Response on success:
{
    "total_amount": 369,
    "discount": 91,
    "net_amount": 344.42,
    "gst": 66.42,
    "items": [
        {
            "total_amount": 240,
            "discount": 36,
            "products": [
                {
                    "product_id": "chicken_curry_cut_small"
                }
            ],
            "type": "individual",
            "quantity": 2,
            "discounting_factor": 0.15
        },
        {
            "total_amount": 220,
            "discount": 55,
            "products": [
                {
                    "product_id": "chicken_curry_cut_small"
                },
                {
                    "product_id": "prawns"
                }
            ],
            "type": "combo",
            "quantity": 1,
            "discounting_factor": 0.25
        }
    ],
    "order_id": "09fc5e22-a510-4c67-b13b-5ec68ae7601b"
}
</code>
<pre>
```
