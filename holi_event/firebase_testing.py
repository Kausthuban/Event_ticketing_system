import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase app (replace with your credentials JSON path)
cred = credentials.Certificate('credentials2.json')
firebase_admin.initialize_app(cred)

# Access Firestore database
db = firestore.client()


# Get a reference to the 'Registrations' collection
collection_ref = db.collection('Registrations')

# Retrieve all documents using get()
docs = collection_ref.get()

# Iterate through the documents and print their data
def get_all_data():
# Create an empty list to store the nested document lists
    collection_list = []
    fields = ['Name','number','generatedTicket','ticketID','totalCount','sentTicket']
    for doc in docs:
        if doc.exists:
            temp = []
            for field in fields:
                temp.append(doc.get(field))
            collection_list.append(temp)
    
    return collection_list



data= get_all_data()
print(data[0])


collection_ref = db.collection('Registrations')
# raw= doc_ref.get()
all_documents = {doc.id: doc.to_dict() for doc in collection_ref.get()}
# Get document data
# if add_id:
#     all_documents = {**all_documents, **{doc.id: {'id': doc.id} for doc in collection_ref.get()}}

# Print the dictionary with all documents
print(all_documents)
# if doc.exists:
#     print("Document data:")
#     print(doc.to_dict()) 


# ['Name','number','generatedTicket','ticketID','totalCount','sentTicket'] Data format