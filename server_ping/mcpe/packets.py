from server_ping.mcpe.data_types import DataTypes

RAKNET_MAGIC = b"\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78"


def encode_serverlist_ping(timestamp):
    return DataTypes.write_byte(0x01) + DataTypes.write_long(timestamp) + RAKNET_MAGIC


def decode_serverlist_pong(buf, offset=0):
    offset, packet_id = DataTypes.read_byte(buf, offset)
    if packet_id != 0x1C:
        raise ValueError("Invalid server reply")

    offset, timestamp = DataTypes.read_long(buf, offset)
    offset, server_id = DataTypes.read_long(buf, offset)
    offset += 16
    offset, info = DataTypes.read_string(buf, offset)
    return info, timestamp