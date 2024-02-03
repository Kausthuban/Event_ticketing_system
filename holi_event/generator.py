import qrcode
from PIL import Image

# Taking the image which the user wants in the QR code center
logo_link = 'logo2.png'
logo = Image.open(logo_link)

# Taking base width
basewidth = 100

# Adjust image size
wpercent = (basewidth / float(logo.size[0]))
hsize = int((float(logo.size[1]) * float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.LANCZOS)

base = '490f960ef20058dfde096436da6897d7'

for id in range(1,10):
    ID = str(id).zfill(4)
    data = base+ID
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

print('QR codes generated!')
