import csv
from . import db
from .models import Product, Tag
def fetch_products():
    with open('website/static/data/Cameras.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Create a new Product instance and set its attributes using the data from the CSV file
            if(row['Product Name']  is not None and len(row['Product Name'])<500 and row['Picture URL'] is not None and row['Price in India'] is not None and row['Description'] is not None):
                # print(row['Product Name'])
                price_str=row['Price in India'] 
                price_str = price_str.replace(",", "") # Remove any commas
                price_str = price_str.replace("₹", "") # Remove the currency symbol
                if(price_str==''):
                    continue
                price_int = int(price_str) # Convert the resulting 
                product = Product(name=row['Product Name'], description=row['Description'], photo=row['Picture URL'], price=price_int, stock=10)
                
                # Create a new Tag instance with the value from the 'Type' column
                tag = Tag(name=row['Type'])
                
                # Add the tag to the product's tags relationship
                product.tags.append(tag)
                
                # Add the product and tag instances to the session and commit the changes to the database
                db.session.add(product)
                db.session.add(tag)
                db.session.commit()