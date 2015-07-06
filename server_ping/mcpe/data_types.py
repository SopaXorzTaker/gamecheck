import struct


class DataTypes(object):
    @staticmethod
    def write_byte(val):
        """
        Encodes a byte
        :param val: A byte value, 0-255
        :type val: int
        :return: The packed value
        :rtype bytes
        """
        return struct.pack("B", val)

    @staticmethod
    def read_byte(buf, offset):
        """
        Decodes a byte
        :param buf: A buffer
        :type buf: bytes
        :return: A tuple, (new offset, value)
        :rtype tuple
        """
        return offset + 1, buf[offset]

    @staticmethod
    def write_short(val):
        """
        Encodes a short
        :param val: A short value, 0-65535
        :type val: int
        :return: The packed value
        :rtype bytes
        """
        return struct.pack("!H", val)

    @staticmethod
    def read_short(buf, offset):
        """
        Decodes a short
        :param buf: A buffer
        :type buf: bytes
        :return: A tuple, (new offset, value)
        :rtype tuple
        """
        return offset + 2, struct.unpack("!H", buf[offset:offset + 2])[0]


    @staticmethod
    def write_int(val):
        """
        Encodes an int
        :param val: An int value, 0-4294967295
        :type val: int
        :return: The packed value
        :rtype bytes
        """
        return struct.pack("!I", val)

    @staticmethod
    def read_int(buf, offset):
        """
        Decodes an int
        :param buf: A buffer
        :type buf: bytes
        :return: A tuple, (new offset, value)
        :rtype tuple
        """
        return offset + 4, struct.unpack("!I", buf[offset:offset + 4])[0]

    @staticmethod
    def write_long(val):
        """
        Encodes a long
        :param val: A long value, 0-429496729
        :type val: int
        :return: The packed value
        :rtype bytes
        """
        return struct.pack("!Q", val)

    @staticmethod
    def read_long(buf, offset):
        """
        Decodes a long
        :param buf: A buffer
        :type buf: bytes
        :return: A tuple, (new offset, value)
        :rtype tuple
        """
        return offset + 8, struct.unpack("!Q", buf[offset:offset + 8])[0]

    @staticmethod
    def write_string(val):
        data = val.encode("utf-8")
        return DataTypes.write_short(len(data)) + data

    @staticmethod
    def read_string(buf, offset):
        offset, length = DataTypes.read_short(buf, offset)
        data = buf[offset:offset + length]
        offset += length
        return offset, data.decode("utf-8")