import json

file_path = "FromPhoneMSG.txt"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

def getencrypted():
    encrypted_value = data["encrypted"]
    print("encrypted:", encrypted_value)
    return encrypted_value
def getivhexData():
    ivhexData_value = data["ivhexData"]
    print("ivhexData:", ivhexData_value)
    return ivhexData_value



