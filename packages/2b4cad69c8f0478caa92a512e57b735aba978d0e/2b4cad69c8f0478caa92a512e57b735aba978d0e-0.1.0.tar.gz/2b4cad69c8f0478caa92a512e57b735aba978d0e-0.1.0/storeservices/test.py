#!/usr/bin/python

import logging
import storeservices
import os
import hashlib
import uuid
from setproctitle import setproctitle

# Wait for user input

adi_proxy = storeservices.StoreServicesCoreADIProxy(
    "/workspaces/apple-private-apis/applemusic", "/workspaces/apple-private-apis/applemusic/adi-data")

# Create random device ID (16 bytes) using Python's os.urandom()
device_id = os.urandom(16)

setproctitle.setproctitle("com.apple.storeuid")
# result = adi_proxy.get_serial_number()
# 
# let mut local_user_uuid_hasher = Sha256::new();
# local_user_uuid_hasher.update(identifier);

local_user_uuid_hasher = hashlib.sha256()
local_user_uuid_hasher.update(device_id)

def convert_hex_to_bytes(external_guid):
    if len(external_guid) > 0:
        # Convert the hexadecimal string to bytes
        hex_bytes = bytes.fromhex(external_guid)
        # Prepend the length divided by 2, followed by three zero bytes
        result = bytes([len(hex_bytes)]) + b'\x00\x00\x00' + hex_bytes
        return result
    else:
        return None  # or some appropriate default value


print('Setting device identifier...')
device = uuid.UUID(bytes=device_id).hex.upper()
guid = str("baa14d7a23294226")


result = adi_proxy.set_device_identifier(
    guid
)

input("Press Enter2 to continue...")

result = adi_proxy.set_fairplay_device_identifier(
    guid
)

# print('Setting set_provisioning_path...')
# result = adi_proxy.set_provisioning_path("/workspaces/apple-private-apis/applemusic/adi-data")

# hex_guid = convert_hex_to_bytes(device)
# print(hex_guid)
# print('Setting set_fireplay_path...')
# result = adi_proxy.set_fireplay_path("/workspaces/apple-private-apis/applemusic/adi-data", hex_guid)


# # result = adi_proxy.set_fairplay_device_identifier(
# #     guid
# # )



# print('Setting provisioning path...')

# # result = adi_proxy.is_machine_provisioned(-2)
# # print(uuid.UUID(bytes=device_id).hex.upper())

# # result = adi_proxy.set_fireplay_path(
# #     ""
# # )

# print('Setting SAP...')

# # result = adi_proxy.setup_sap()



# # print(result)


# # adi_proxy.set_device_identifier(
# #     uuid::Uuid::from_bytes(identifier)
# #         .to_string()
# #         .to_uppercase(),
# # )?; // UUID, uppercase
# # adi_proxy
#     # .set_local_user_uuid(hex::encode(local_user_uuid_hasher.finalize()).to_uppercase()); // 64 uppercase character hex

# # 
# # otp = adi_proxy.request_otp(-2)
# # print(otp)
