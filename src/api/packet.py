import struct


class Packet:

    def __init__(self, cmd: int, flags: int, length: int, data: bytes,
                 fmt: str = None):
        self.cmd = cmd
        self.flags = flags
        self.length = length
        self.data = data
        self._fmt = fmt

    def __repr__(self):
        return f'| {self.cmd} | {self.flags} | {self.length} | {self.data} |'

    def to_bytes(self) -> bytearray:
        header = struct.pack(self._fmt, self.cmd, self.flags, self.length)
        return bytearray(header + self.data)
