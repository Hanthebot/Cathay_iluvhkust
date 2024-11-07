""" for QR code generation """
from qrcode import make

def generate_qr(data: str) -> str:
    """ generates QR """
    img = make(data)
    title = f"/img/qr/qr_{data}.png"
    img.save("./static" + title)
    return title
