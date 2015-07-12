from server_ping.minecraft.data_types import DataTypes


def encode_packet(packet_id, data):
    """
    Encodes a packet payload
    :param packet_id: Packet ID
    :type packet_id: int
    :param data: Data
    :type data: bytes
    :return: The encoded payload
    :rtype: bytes
    """
    payload = DataTypes.write_varint(packet_id) + data
    return DataTypes.write_varint(len(payload)) + payload


def decode_packet(buf, offset):
    """
    Decodes a packet payload
    :param buf: The source buffer
    :type buf: bytes
    :param offset: Buffer offset
    :type offset: int
    :return: 2-tuple (new offset, (packet_id, packet_payload))
    :rtype tuple
    """
    #print(buf, offset)
    offset, length = DataTypes.read_varint(buf, offset)
    #print(length)
    payload = buf[offset:offset + length]
    #if len(payload) < 16:
    #    print(payload)
    offset += length
    payload_offset, packet_id = DataTypes.read_varint(payload, 0)
    data = payload[payload_offset:]
    return offset, (packet_id, data)


def encode_handshake(protocol_version, server_address, server_port, next_state):
    return encode_packet(0x00, DataTypes.write_varint(protocol_version) +
            DataTypes.write_string(server_address) + DataTypes.write_short(server_port) +
            DataTypes.write_varint(next_state)
    )


def encode_request():
    return encode_packet(0x00, b"")


def encode_ping(timestamp):
    return encode_packet(0x01, DataTypes.write_long(timestamp))


def decode_response(buf, offset=0):
    offset, packet = decode_packet(buf, offset)
    if packet[0] != 0x00:
        raise ValueError("Invalid packet %s" % hex(packet[0])[2:].zfill(2))

    payload = packet[1]
    response = DataTypes.read_string(payload, 0)[1]
    return offset, response


def decode_pong(buf, offset=0):
    offset, packet = decode_packet(buf, offset)
    # Wiki.vg says that the ID is 0x00, but the actual server gave 0x01
    if packet[0] not in [0x00, 0x01]:
        raise ValueError("Invalid packet %s" % hex(packet[0])[2:].zfill(2))

    payload = packet[1]
    timestamp = DataTypes.read_long(payload, 0)[1]
    return offset, timestamp