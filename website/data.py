import csv
from . import db
from .models import Product, Tag, Seller
from werkzeug.security import generate_password_hash

def fetch_products():
    # Check if a seller with email 'admin@admin.com' exists
    seller = Seller.query.filter_by(email='admin@admin.com').first()
    if seller:
        # If seller exists, return their seller_id
        return
    else:
        # If seller does not exist, create a new one
        # Create an admin seller
        admin_seller = Seller(
            first_name='Admin',
            last_name='Seller',
            email='admin@admin.com',
            password=generate_password_hash("password", method='sha256'),
            address='Girnar',
            phone_number=1234567890,
            aadhar=123456789010
        )

        # Add the admin seller to the database
        db.session.add(admin_seller)
        db.session.commit()
        seller_id = admin_seller.id

        # Use the seller_id as needed
        print("Admin seller_id",seller_id)


        with open('website/static/data/mobiles.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if all required keys are present in the dictionary
                if 'Product Name' in row and 'Picture URL' in row and 'Price in India' in row and 'Description' in row and row['Product Name'] is not None and len(row['Product Name']) < 500 and row['Picture URL'] is not None and row['Price in India'] is not None and row['Description'] is not None:
                    # Create a new Product instance and set its attributes using the data from the CSV file
                    price_str = row['Price in India'] 
                    price_str = price_str.replace(",", "") # Remove any commas
                    price_str = price_str.replace("₹", "") # Remove the currency symbol
                    if price_str == '':
                        continue

                    price_int = int(price_str) # Convert the resulting 
                    product = Product(name=row['Product Name'], description=row['Description'], photo=row['Picture URL'], price=price_int, stock=10,seller_id=seller_id, type='Mobile')

                    # Create a new Tag instance with the value from the 'Type' column
                    tag = Tag(name=row['Type'])
                    # Add the tag to the product's tags relationship
                    product.tags.append(tag)
                    db.session.add(product)
                    db.session.add(tag)
                    db.session.commit()
        print(1)
        with open('website/static/data/tablets.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if all required keys are present in the dictionary
                if 'Product Name' in row and 'Picture URL' in row and 'Price in India' in row and 'Description' in row and row['Product Name'] is not None and len(row['Product Name']) < 500 and row['Picture URL'] is not None and row['Price in India'] is not None and row['Description'] is not None:
                    # Create a new Product instance and set its attributes using the data from the CSV file
                    price_str = row['Price in India'] 
                    price_str = price_str.replace(",", "") # Remove any commas
                    price_str = price_str.replace("₹", "") # Remove the currency symbol
                    if price_str == '':
                        continue

                    price_int = int(price_str) # Convert the resulting 
                    product = Product(name=row['Product Name'], description=row['Description'], photo=row['Picture URL'], price=price_int, stock=10,seller_id=seller_id, type='Tablet')

                    # Create a new Tag instance with the value from the 'Type' column
                    tag = Tag(name=row['Type'])
                    # Add the tag to the product's tags relationship
                    product.tags.append(tag)
                    db.session.add(product)
                    db.session.add(tag)
                    db.session.commit()
        print(2)
        with open('website/static/data/gaming_consoles.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if all required keys are present in the dictionary
                if 'Product Name' in row and 'Picture URL' in row and 'Price in India' in row and 'Description' in row and row['Product Name'] is not None and len(row['Product Name']) < 500 and row['Picture URL'] is not None and row['Price in India'] is not None and row['Description'] is not None:
                    # Create a new Product instance and set its attributes using the data from the CSV file
                    price_str = row['Price in India'] 
                    price_str = price_str.replace(",", "") # Remove any commas
                    price_str = price_str.replace("₹", "") # Remove the currency symbol
                    if price_str == '':
                        continue

                    price_int = int(price_str) # Convert the resulting 
                    product = Product(name=row['Product Name'], description=row['Description'], photo=row['Picture URL'], price=price_int, stock=10,seller_id=seller_id, type='Gaming Console')

                    # Create a new Tag instance with the value from the 'Type' column
                    tag = Tag(name=row['Type'])
                    # Add the tag to the product's tags relationship
                    product.tags.append(tag)
                    db.session.add(product)
                    db.session.add(tag)
                    db.session.commit()
        
        print(3)
        with open('website/static/data/laptops.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if all required keys are present in the dictionary
                if 'Product Name' in row and 'Picture URL' in row and 'Price in India' in row and 'Description' in row and row['Product Name'] is not None and len(row['Product Name']) < 500 and row['Picture URL'] is not None and row['Price in India'] is not None and row['Description'] is not None:
                    # Create a new Product instance and set its attributes using the data from the CSV file
                    price_str = row['Price in India'] 
                    price_str = price_str.replace(",", "") # Remove any commas
                    price_str = price_str.replace("₹", "") # Remove the currency symbol
                    if price_str == '':
                        continue

                    price_int = int(price_str) # Convert the resulting 
                    product = Product(name=row['Product Name'], description=row['Description'], photo=row['Picture URL'], price=price_int, stock=10,seller_id=seller_id, type='Laptop')

                    # Create a new Tag instance with the value from the 'Type' column
                    tag = Tag(name=row['Type'])
                    # Add the tag to the product's tags relationship
                    product.tags.append(tag)
                    db.session.add(product)
                    db.session.add(tag)
                    db.session.commit()

        
        print(4)
        with open('website/static/data/televisions.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Check if all required keys are present in the dictionary
                if 'Product Name' in row and 'Picture URL' in row and 'Price in India' in row and 'Description' in row and row['Product Name'] is not None and len(row['Product Name']) < 500 and row['Picture URL'] is not None and row['Price in India'] is not None and row['Description'] is not None:
                    # Create a new Product instance and set its attributes using the data from the CSV file
                    price_str = row['Price in India'] 
                    price_str = price_str.replace(",", "") # Remove any commas
                    price_str = price_str.replace("₹", "") # Remove the currency symbol
                    if price_str == '':
                        continue

                    price_int = int(price_str) # Convert the resulting 
                    product = Product(name=row['Product Name'], description=row['Description'], photo=row['Picture URL'], price=price_int, stock=10,seller_id=seller_id, type='Television')

                    # Create a new Tag instance with the value from the 'Type' column
                    tag = Tag(name=row['Type'])
                    # Add the tag to the product's tags relationship
                    product.tags.append(tag)
                    db.session.add(product)
                    db.session.add(tag)
                    db.session.commit()

                    