import json

file_path = "FromPhoneMSG.txt"

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

encrypted_value = data["encrypted"]
ivhexData_value = data["ivhexData"]

print("encrypted:", encrypted_value)
print("ivhexData:", ivhexData_value)
