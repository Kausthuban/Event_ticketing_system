import csv
import pywhatkit as kit
import time

# Read phone numbers from CSV file
def send_message(ticketID,number):
    message = "Dear customer, thank you for choosing event managers for the holi event on 25th"
    #kit.sendwhatmsg_instantly("+91"+row[1],message.format(data[0],data[2]), 10, tab_close=True)
    kit.sendwhats_image("+91"+number, "Codes/0001.png",message, 10, tab_close=True)
    time.sleep(4)  # Wait for a few seconds between messages


