# Imports 

import pywhatkit as kit
import time
import qrcode
from PIL import Image
import firebase_admin
from firebase_admin import credentials, firestore
import hashlib
from datetime import datetime
# Initializations 

cred = credentials.Certificate('credentials2.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
Registrations = db.collection('Registrations')
Tickets = db.collection('QR_Codes')
# IDCounter = db.get('counterDocument')
logo_link = 'logo2.png'
logo = Image.open(logo_link)
reg_write_template = {'Name': '', 'Date': datetime.now(), 'amount': 300, 'totalCount': 8, 'number': '9944524545', 'ticketID': '', 'generatedTicket': False, 'sentTicket': False, 'imageID': ''}
idcount_doc = db.collection('Registrations').document('counterDocument')
idcount = idcount_doc.get()

# Functions 

def hashing(msg):
    hashval = hashlib.sha1(msg.encode("UTF-8")).hexdigest()
    return hashval[:10]

def send_message(ticketID,number,imageID):
    message = "Dear customer, thank you for choosing event managers for the holi event on 25th"
    kit.sendwhats_image("+91"+number, "Codes/imageID.png",message, 10, tab_close=True)
    time.sleep(4)

def generate_ticket(data,template,ID):
    base = 'holi_'
    raw = base+data[1]
    ID = hashing(base+data[1])
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
    QRimg.save(f'Codes/{ID}.png')
        
    return ID


def get_all_data(): #Input the document to be read/processed
    collection_list = []
    fields = ['Name','number','generatedTicket','ticketID','totalCount','sentTicket']
    for doc in Registrations:
        if doc.exists:
            temp = []
            for field in fields:
                temp.append(doc.get(field))
            collection_list.append(temp)
    
    return collection_list

def write_columns(collection,columns,ID,data):
    to_set = {}
    doc_ref = collection.document(ID)
    for field in columns:
        if field in data:
            to_set[field] = data[field]
    doc_ref.set(to_set)


def write_document(collection,ID,data):
    # Create a document reference with the custom ID
    doc_ref = collection.document(ID)
    # Set the data on the document
    doc_ref.set(data)

def ticket_not_generated(data):
    res = []
    for row in data:
        if row[2] == False:
            res.append(row)
        
    return res




for i in range(3):
    reg_docs = Registrations.get()
    ticket_docs = Tickets.get()
    all = get_all_data()
    no_tickets = ticket_not_generated(all)
    print(no_tickets)
    for i in no_tickets:
        pass
    # print(idcount.get('userID'))








# Formats
    
    # write for Registrations {'Name': 'Radha', 'Date': datetime.now(), 'amount': 300, 'totalCount': 8, 'number': '9944524545', 'ticketID': '', 'generatedTicket': False, 'sentTicket': False, 'imageID': ''}