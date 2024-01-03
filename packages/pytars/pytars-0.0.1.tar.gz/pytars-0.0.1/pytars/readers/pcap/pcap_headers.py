"""PCAP file headers."""

import struct
from dataclasses import dataclass
from typing import Optional

import numpy as np


def hex_str_with_periods(x: bytes) -> str:
    """Convert bytes to hex string with periods between each byte."""
    return ".".join([str(x) for x in struct.unpack("B" * len(x), x)])


def hex_str_with_colons(x: bytes) -> str:
    """Convert bytes to hex string with colons between each byte."""
    return ":".join([hex(x)[2:].zfill(2) for x in struct.unpack("B" * len(x), x)])


class GlobalHeader:
    """Global Header for PCAP file."""

    def __init__(self, data: bytes):
        # type hints
        self.magic_number: int
        self.version_major: int
        self.version_minor: int
        self.timezone: int
        self.timestamp_accuracy: int
        self.snapshot_length: int
        self.link_layer_type: int

        # check data size
        EXPECTED_DATA_SIZE = 24
        if len(data) < EXPECTED_DATA_SIZE:
            raise ValueError("Global Header data is too short.")

        # parse data
        (
            self.magic_number,
            self.version_major,
            self.version_minor,
            self.timezone,
            self.timestamp_accuracy,
            self.snapshot_length,
            self.link_layer_type,
        ) = struct.unpack("<IHHiiII", data[:EXPECTED_DATA_SIZE])

    def __str__(self) -> str:
        return (
            "GlobalHeader(\n"
            f"  magic_number={hex(self.magic_number)},\n"
            f"  version_major={self.version_major},\n"
            f"  version_minor={self.version_minor},\n"
            f"  timezone={self.timezone},\n"
            f"  timestamp_accuracy={self.timestamp_accuracy},\n"
            f"  snapshot_length={self.snapshot_length},\n"
            f"  link_layer_type={self.link_layer_type}\n"
            ")"
        )

    __repr__ = __str__


class PacketHeader:
    """Packet Header for PCAP file packets."""

    def __init__(self, data: bytes, start_time: Optional[float] = None):
        # type hints
        self._packet_timestamp_second: int
        self._packet_timestamp_microseconds: int
        self.capture_length: int
        self.original_length: int
        self.relative_timestamp_seconds: float

        # check data size
        EXPECTED_DATA_SIZE = 16
        if len(data) < EXPECTED_DATA_SIZE:
            raise ValueError("Packet Header data is too short.")

        # parse data
        (
            self._packet_timestamp_second,
            self._packet_timestamp_microseconds,
            self.capture_length,
            self.original_length,
        ) = struct.unpack("<IIII", data[:EXPECTED_DATA_SIZE])
        if start_time is not None:
            self.relative_timestamp_seconds = self.timestamp_seconds - start_time
        else:
            self.relative_timestamp_seconds = self.timestamp_seconds

    @property
    def datetime(self) -> np.ndarray:
        return np.array(self.timestamp_seconds * 1e6).astype("datetime64[us]")

    @property
    def timestamp_seconds(self) -> float:
        return self._packet_timestamp_second + self._packet_timestamp_microseconds / 1e6

    def __str__(self) -> str:
        return (
            "PacketHeader(\n"
            f"  datetime={self.datetime},\n"
            f"  relative_timestamp_seconds={self.relative_timestamp_seconds},\n"
            f"  capture_length={self.capture_length},\n"
            f"  original_length={self.original_length}\n"
            ")"
        )

    __repr__ = __str__


class Ethernet2Header:
    """Ethernet 2 Header for PCAP file packets."""

    def __init__(self, data: bytes):
        # type hints
        self.destination_mac_addr: bytes
        self.source_mac_addr: bytes
        self.ether_type: int

        # check data size
        EXPECTED_DATA_SIZE = 14
        if len(data) < EXPECTED_DATA_SIZE:
            raise ValueError("Ethernet 2 Header data is too short.")

        # parse data
        (
            self.destination_mac_addr,
            self.source_mac_addr,
            self.ether_type,
        ) = struct.unpack("!6s6sH", data[:EXPECTED_DATA_SIZE])

    @property
    def destination_mac_addr_str(self) -> str:
        return hex_str_with_colons(self.destination_mac_addr)

    @property
    def source_mac_addr_str(self) -> str:
        return hex_str_with_colons(self.source_mac_addr)

    @property
    def is_vlan(self) -> bool:
        return self.ether_type == 0x8100

    @property
    def is_ipv4(self) -> bool:
        return self.ether_type == 0x0800

    def __str__(self) -> str:
        return (
            "Ethernet2Header(\n"
            f"  destination_mac_addr={self.destination_mac_addr_str},\n"
            f"  source_mac_addr={self.source_mac_addr_str},\n"
            f"  ether_type={hex(self.ether_type)}\n"
            ")"
        )

    __repr__ = __str__


class VLANHeader:
    """VLAN Header for PCAP file packets."""

    def __init__(self, data: bytes):
        # type hints
        self.priority_code_point: int
        self.drop_eligible_indicator: int
        self.vlan_id: int

        # check data size
        EXPECTED_DATA_SIZE = 4
        if len(data) < EXPECTED_DATA_SIZE:
            raise ValueError("VLAN Header data is too short.")

        # parse data
        tag_control_info = struct.unpack("!H", data[:2])[0]
        self.priority_code_point = (tag_control_info >> 13) & 0x7
        self.drop_eligible_indicator = (tag_control_info >> 12) & 0x1
        self.vlan_id = tag_control_info & 0xFFF
        self.next_ether_type = struct.unpack("!H", data[2:4])[0]

    @property
    def is_ipv4(self) -> bool:
        return self.next_ether_type == 0x0800

    def __str__(self) -> str:
        return (
            "VLANHeader(\n"
            f"  priority_code_point={self.priority_code_point},\n"
            f"  drop_eligible_indicator={self.drop_eligible_indicator},\n"
            f"  vlan_id={self.vlan_id}\n"
            ")"
        )

    __repr__ = __str__


class IPv4Header:
    """IPv4 Header for PCAP file packets."""

    def __init__(self, data: bytes):
        # type hints
        self.version: int
        self.header_length: int
        self.type_of_service: int
        self.total_length: int
        self.id: int
        self.flags: IPv4Flags
        self.fragment_offset: int
        self.ttl: int
        self.protocol: int
        self.header_checksum: int
        self.source_ip_address: bytes
        self.destination_ip_address: bytes
        self.options: Optional[bytes]

        # check data size
        EXPECTED_DATA_SIZE = 20
        if len(data) < EXPECTED_DATA_SIZE:
            raise ValueError("IPv4 Header data is too short.")

        # parse data
        (
            version_ihl,
            self.type_of_service,
            self.total_length,
            self.id,
            flags_fragment_offset,
            self.ttl,
            self.protocol,
            self.header_checksum,
            self.source_ip_address,
            self.destination_ip_address,
        ) = struct.unpack("!BBHHHBBH4s4s", data[:EXPECTED_DATA_SIZE])

        self.version = version_ihl >> 4
        self.header_length = version_ihl & 0xF
        self.flags = IPv4Flags(flags_fragment_offset >> 13)
        self.fragment_offset = flags_fragment_offset & 0x1FFF

        header_length = self.header_length * 4
        if header_length > EXPECTED_DATA_SIZE:
            options_length = header_length - EXPECTED_DATA_SIZE
            self.options = data[EXPECTED_DATA_SIZE : EXPECTED_DATA_SIZE + options_length]
        else:
            self.options = None

    @property
    def source_ip_address_str(self) -> str:
        return hex_str_with_periods(self.source_ip_address)

    @property
    def destination_ip_address_str(self) -> str:
        return hex_str_with_periods(self.destination_ip_address)

    @property
    def is_udp(self) -> bool:
        return self.protocol == 17

    def __str__(self) -> str:
        return (
            "IPv4Header(\n"
            f"  version={self.version},\n"
            f"  header_length={self.header_length},\n"
            f"  type_of_service={self.type_of_service},\n"
            f"  total_length={self.total_length},\n"
            f"  id={self.id},\n"
            f"  flags={self.flags},\n"
            f"  fragment_offset={self.fragment_offset},\n"
            f"  ttl={self.ttl},\n"
            f"  protocol={self.protocol},\n"
            f"  header_checksum={self.header_checksum},\n"
            f"  source_ip_address={self.source_ip_address_str},\n"
            f"  destination_ip_address={self.destination_ip_address_str},\n"
            f"  options={self.options}\n"
            ")"
        )

    __repr__ = __str__


class IPv4Flags:
    """IPv4 Flags for PCAP file packets."""

    def __init__(self, data: int):
        # type hints
        self.reserved: bool
        self.dont_fragment: bool
        self.more_fragments: bool

        # parse data
        self.reserved = bool((data >> 2) & 0x1)
        self.dont_fragment = bool((data >> 1) & 0x1)
        self.more_fragments = bool(data & 0x1)

    def __str__(self) -> str:
        return (
            "IPv4Flags(\n"
            f"  reserved={self.reserved},\n"
            f"  dont_fragment={self.dont_fragment},\n"
            f"  more_fragments={self.more_fragments}\n"
            ")"
        )

    __repr__ = __str__


class PTPv2:
    """PTPv2 Header for PCAP file packets."""

    def __init__(self, data: bytes):
        # type hints
        self.transport_specific: int
        self.message_type: int
        self.version_ptp: int
        self.message_length: int
        self.domain_number: int
        self.reserved: int
        self.flags: int
        self.correction_field: int
        self.reserved2: int
        self.source_port_identity: int
        self.sequence_id: int
        self.control_field: int
        self.log_message_interval: int

        # check length
        EXPECTED_LENGTH = 34
        if len(data) != EXPECTED_LENGTH:
            raise ValueError(f"PTPv2 Header length [{len(data)}] != [{EXPECTED_LENGTH}]")

        # parse data
        (
            self.transport_specific,
            self.message_type,
            self.version_ptp,
            self.message_length,
            self.domain_number,
            self.reserved,
            self.flags,
            self.correction_field,
            self.reserved2,
            self.source_port_identity,
            self.sequence_id,
            self.control_field,
            self.log_message_interval,
        ) = struct.unpack("!BBBHBHQQQHHB", data[:EXPECTED_LENGTH])

    def __str__(self) -> str:
        return f"PTPv2(transport_specific={self.transport_specific}, message_type={self.message_type}, version_ptp={self.version_ptp}, message_length={self.message_length}, domain_number={self.domain_number}, reserved={self.reserved}, flags={self.flags}, correction_field={self.correction_field}, reserved2={self.reserved2}, source_port_identity={self.source_port_identity}, sequence_id={self.sequence_id}, control_field={self.control_field}, log_message_interval={self.log_message_interval})"

    __repr__ = __str__


class UDPHeader:
    """UDP Header for PCAP file packets."""

    def __init__(self, data: bytes):
        # type hints
        self.source_port: int
        self.destination_port: int
        self.length: int
        self.checksum: int

        # check data size
        EXPECTED_DATA_SIZE = 8
        if len(data) < EXPECTED_DATA_SIZE:
            raise ValueError("UDP Header data is too short.")
        # parse data
        (self.source_port, self.destination_port, self.length, self.checksum) = struct.unpack(
            "!HHHH", data[:EXPECTED_DATA_SIZE]
        )

    def __str__(self) -> str:
        return (
            "UDPHeader(\n"
            f"  source_port={self.source_port},\n"
            f"  destination_port={self.destination_port},\n"
            f"  length={self.length},\n"
            f"  checksum={self.checksum}\n"
            ")"
        )

    __repr__ = __str__


class UDPData:
    """UDP Data for PCAP file packets."""

    def __init__(self, data: bytes):
        self.data = data

    def __str__(self) -> str:
        return f"UDPData(data=[{len(self.data)} bytes])"

    __repr__ = __str__


@dataclass
class PcapPacket:
    """All headers for PCAP file packets."""

    packet_ind: int = -1
    packet_header: Optional[PacketHeader] = None
    ethernet_header: Optional[Ethernet2Header] = None
    vlan_header: Optional[VLANHeader] = None
    ipv4_header: Optional[IPv4Header] = None
    ptpv2: Optional[PTPv2] = None
    udp_header: Optional[UDPHeader] = None
    udp_data: Optional[UDPData] = None
