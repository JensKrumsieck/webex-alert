import qrcode as qrc

def qrcode(uri: str):
    qr = qrc.QRCode()
    qr.add_data(uri)
    qr.make(fit=True)
    qr.print_ascii()