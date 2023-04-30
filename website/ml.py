# from . import db
# from .models import User, Product, CartItems, OrderItems, SearchHistory
# from lightfm import LightFM
# from lightfm.data import Dataset
# import numpy as np
# from scipy.sparse import csr_matrix

# def recommendations(user_id):
# 	type_to_number = {'Television':0,'Mobile':1,'Laptop':2,'Tablet':3,'Gaming Console':4}

# 	users = User.query.all()
# 	products = Product.query.all()
# # "34,45,67,9890,"
# 	dataset = Dataset()
# 	dataset.fit(users=[u.id for u in users], items=[p.id for p in products])

	
# 	search_history = SearchHistory.query.all()
# 	search_final =[]
# 	for i in search_history:
# 		a = i.searches.split(',')
# 	# list of string to int
# 		a = list(map(int, a))
# 		for k in a:
# 			search_final.append([i.user_id,k])

		
# 	# user_product_matrix = dataset.build_interactions((user_id,product_id) for product_id in search_history)


# 	# user_product_matrix = dataset.build_interactions((ci.user_id,ci.product_id) for ci in CartItems.query.all())
# 	# user_product_matrix += dataset.build_interactions((oi.user_id,oi.product_id) for oi in OrderItems.query.all())
# 	# user_product_matrix += dataset.build_interactions((c[0],c[1]) for c in search_final)


# 	# from scipy.sparse import concatenate
# 	# user_product_matrix = csr_matrix(user_product_matrix)
# 	user_product_matrix = dataset.build_interactions((ci.user_id, ci.product_id) for ci in CartItems.query.all())
# 	user_product_matrix = np.concatenate([user_product_matrix, dataset.build_interactions((oi.user_id, oi.product_id) for oi in OrderItems.query.all())], axis=0)
# 	user_product_matrix = np.concatenate([user_product_matrix, dataset.build_interactions((c[0], c[1]) for c in search_final)], axis=0)
# 	product_features = np.zeros((len(products),7))
# 	user_product_matrix = csr_matrix(user_product_matrix, shape=(len(users), len(products)))

# 	for i, product in enumerate(products):
# 		type = product.type
# 		if type in type_to_number:
# 			product_features[i,type_to_number[type]]=1
# 		product_features[i,5]=product.price
# 		# product_features[i,6]=product.rating

	
# 	model = LightFM(loss='warp')
# 	model.fit(user_product_matrix, item_features=product_features, epochs=10)

# 	user_index = dataset.mapping()[0][user_id]
# 	scores = model.predict(user_index,np.arange(len(products)),item_features=product_features)

# 	top_products = sorted(zip(products,scores),key=lambda x:x[1],reverse=True)[:9]

# 	return top_products











########## new code erroneous ##########








# from . import db
# from .models import User, Product, CartItems, OrderItems, SearchHistory
# from lightfm import LightFM
# from lightfm.data import Dataset
# import numpy as np
# import scipy.sparse as sp

# def recommendations(user_id):
#     type_to_number = {'Television':0,'Mobile':1,'Laptop':2,'Tablet':3,'Gaming Console':4}

#     users = User.query.all()
#     products = Product.query.all()

#     dataset = Dataset()
#     dataset.fit(users=[u.id for u in users], items=[p.id for p in products])

#     search_history = SearchHistory.query.all()
#     search_final =[]
#     for i in search_history:
#         a = i.searches.split(',')
#         a = list(map(int, a))
#         for k in a:
#             if i.user_id < len(users) and k < len(products):
#                 search_final.append((i.user_id,k))

#     if search_final:
#         rows, cols = zip(*search_final)
#         data = np.ones(len(rows))

#         user_product_matrix = sp.coo_matrix((data, (rows, cols)), shape=(len(users), len(products)))
#         for ci in CartItems.query.all():
#             user_product_matrix[ci.user_id, ci.product_id] = 1
#         for oi in OrderItems.query.all():
#             user_product_matrix[oi.user_id, oi.product_id] = 1

#         product_features = np.zeros((len(products),7))
#         for i, product in enumerate(products):
#             type = product.type
#             if type in type_to_number:
#                 product_features[i,type_to_number[type]]=1
#             product_features[i,5]=product.price
#             # product_features[i,6]=product.rating

#         model = LightFM(loss='warp')
#         model.fit(user_product_matrix, item_features=product_features, epochs=10)

#         user_index = dataset.mapping()[0][user_id]
#         scores = model.predict(user_index,np.arange(len(products)),item_features=product_features)

#         top_products = sorted(zip(products,scores),key=lambda x:x[1],reverse=True)[:9]

#         return top_products
#     else:
#         return []