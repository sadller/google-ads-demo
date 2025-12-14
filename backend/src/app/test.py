from google.ads.googleads.client import GoogleAdsClient


client = GoogleAdsClient.load_from_storage("google-ads.yaml")
ga_service = client.get_service("GoogleAdsService")
query = """
    SELECT
        customer.id,
        customer.descriptive_name
    FROM customer
"""
customer_id = "2121758184"
response = ga_service.search(customer_id=customer_id, query=query)
for row in response:
    print(row.customer.id, row.customer.descriptive_name)
