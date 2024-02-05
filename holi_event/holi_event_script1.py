# %%
import os
import pywhatkit as kit
import time
import qrcode
from PIL import Image
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
from datetime import datetime

# %%
cred = credentials.Certificate('credentials2.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# %%
Registrations = db.collection('Registrations')
Tickets = db.collection('QR_Codes')
# IDCounter = db.get('counterDocument')
logo_link = 'logo2.png'
logo = Image.open(logo_link)

idcount_doc = db.collection('Registrations').document('counterDocument')
# idcount = idcount_doc.get().get('userCount')
counter_doc = db.collection('Logs_Variables').document('docCounter')

# %%
reg_template = {'Name': '', 'Date': datetime.now(), 'amount': 300, 'totalCount': 0, 'number': '', 'ticketID': '', 'generatedTicket': False, 'sentTicket': False, 'imageID': ''}
tkt_template = {'totalCount' : 0, 'visitedCount' : 0, 'used':False, 'timestamp' : ''}

def get_count():
    idcount_doc = db.collection('Logs_Variables').document('docCounter')
    idcount = idcount_doc.get().get('userCount')
    return idcount

def inc_count():
    counter_doc.update({'userCount': firestore.Increment(1)})

def hash_gen(data):
        hashval = hashlib.sha1(data.encode("UTF-8")).hexdigest()
        return hashval

def gen_qr(data,imgID,logo=logo):
    basewidth = 100

    # Adjust image size
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.LANCZOS)

    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    QRcode.add_data(data)
    QRcode.make()

    QRcolor = 'Black'
    QRimg = QRcode.make_image(
        fill_color=QRcolor, back_color="white").convert('RGBA')

    pos = ((QRimg.size[0] - logo.size[0]) // 2,
        (QRimg.size[1] - logo.size[1]) // 2)

    # Paste the logo onto the QR code with transparency
    QRimg.paste(logo, pos, logo)

    # Save the QR code generated
    QRimg.save(f'Codes/{imgID}.png')


def add_tkt_entry(ID,totalCount,tkt_template=tkt_template):
     doc_ref = db.collection("QR_Codes").document(ID)
     tkt_template['totalCount'] = totalCount
     tkt_template['timestamp'] = firestore.SERVER_TIMESTAMP
     doc_ref.set(tkt_template)

# %%
def send_message(ticketID,number,imageID):
    message = f"Dear customer,\n\n We extend our sincere gratitude for selecting MSLASH Event Management to coordinate the upcoming Holi event \"HOLI CLOUDS\" scheduled for the 25th Of March.\n\nYour assigned Ticket ID is provided below. Please make sure to show up to the event from 9 am to 4 pm\n \n {ticketID}"
    kit.sendwhats_image("+91"+number, f"Codes/{imageID}",message,50,True,5)
    time.sleep(4)

# %%

# Working Ticket Generator
def generate_ticket(docID,tkt_template=tkt_template,base_txt='holi_event_'):
    # Get the Document
    reg_doc = db.collection('Registrations').document(docID)
    # Check the codition
    if reg_doc.get().get('generatedTicket'):
        return
    # Get counter value
    count = get_count()
    counter = str(count).zfill(3)
    # Generate ID and QR
    ID = hash_gen(base_txt+counter)
    gen_qr(ID,counter)
    # Get the existing data and modify the required fields
    new_reg_doc = db.collection('Registrations').document(docID).get().to_dict()
    new_reg_doc['ticketID'] = ID
    new_reg_doc['generatedTicket'] = True
    new_reg_doc['imageID'] = counter+'.png'
    # Update the new values
    reg_doc.set(new_reg_doc)
    # Increment the counter
    inc_count()
    # Create a new entry in the Tickets_page
    add_tkt_entry(ID,reg_doc.get().get('totalCount'))


# %%
# Sending Message in whatsapp

def send_message_to_id(docID):
    reg_doc = db.collection('Registrations').document(docID)
    if reg_doc.get().get('sentTicket'):
        return
    imageID = reg_doc.get().get('imageID')
    ticketID = reg_doc.get().get('ticketID')
    number = reg_doc.get().get('number')
    send_message(ticketID,number,imageID)
    new_reg_doc = db.collection('Registrations').document(docID).get().to_dict()
    new_reg_doc['sentTicket'] = True
    # Update the new values
    reg_doc.set(new_reg_doc)

    
    



# %%
def get_ids(collection_name='Registrations'):
    collection_ref = db.collection(collection_name)
    # Get all documents in the collection
    docs = collection_ref.get()
    # Create an empty list to store document IDs
    document_ids = []
    # Extract document IDs from each document
    for doc in docs:
        document_ids.append(doc.id)
    return document_ids

def check_deleted():
    present =[]
    for id in get_ids():
        file= db.collection('Registrations').document(id)
        print(file.get().get('imageID'))
        present.append(file.get().get('imageID'))



    folder_path = 'Codes/'
    all_files = os.listdir(folder_path)
    print(present)
    for file_name in all_files:
    
        if file_name not in present:
        # Construct the full path to the file
            file_path = os.path.join(folder_path, file_name)
            try:
            # Attmpt to delete the file
                print(file_name)
                #os.remove(file_path)
            except OSError as e:
                pass
# %%
def get_exec():
    idcount_doc = db.collection('Logs_Variables').document('Execute')
    idcount = idcount_doc.get().get('execute')
    return idcount
def update_exec():
    idcount_doc = db.collection('Logs_Variables').document('Execute')
    # Update the 'execute' field to False
    idcount_doc.update({'execute': False})

def main():
    for id in get_ids():
        print(id)
        generate_ticket(id)
        send_message_to_id(id)


while True:
    check_deleted()    
    main()
    time.sleep(30)
        

