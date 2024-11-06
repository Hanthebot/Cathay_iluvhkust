from pyzbar.pyzbar import decode

def BarcodeReader(image):
    """ barcode rea """
    decoded_objects = decode(image)
    if decoded_objects:
        obj = decoded_objects[0]
        return (obj.data.decode('utf-8'), obj.type)
    return None