import qrcode


def generate_ticket_qr(ticket_id):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4,
    )

    qr.add_data(str(ticket_id))
    qr.make(fit=True)

    return qr.make_image()
