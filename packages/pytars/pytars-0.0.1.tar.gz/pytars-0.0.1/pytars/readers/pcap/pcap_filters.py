from dataclasses import dataclass
from typing import Optional, Tuple

import numpy as np


@dataclass
class PcapPacketFilters:
    """A class to hold the filters for a pcap file."""

    max_packets: Optional[int] = 999_999_999
    source_ip_addr: Optional[str] = None
    source_mac_addr: Optional[str] = None
    source_port: Optional[int] = None
    destination_ip_addr: Optional[str] = None
    destination_mac_addr: Optional[str] = None
    destination_port: Optional[int] = None
    relative_time_gate_seconds: Optional[Tuple[float]] = None
    datetime_gate: Optional[Tuple[np.ndarray]] = None
    udp_payload_length_gate: Optional[Tuple[int]] = None

    def __str__(self) -> str:
        return (
            "PcapFilters(\n"
            f"  max_packets={self.max_packets},\n"
            f"  source_ip_addr={self.source_ip_addr},\n"
            f"  source_mac_addr={self.source_mac_addr},\n"
            f"  source_port={self.source_port},\n"
            f"  destination_ip_addr={self.destination_ip_addr},\n"
            f"  destination_mac_addr={self.destination_mac_addr},\n"
            f"  destination_port={self.destination_port},\n"
            f"  relative_time_gate_seconds={self.relative_time_gate_seconds},\n"
            f"  datetime_gate={self.datetime_gate}\n"
            f"  udp_payload_bytes_gate={self.udp_payload_length_gate}\n"
            ")"
        )

    def copy(self) -> "PcapPacketFilters":
        return PcapPacketFilters(
            max_packets=self.max_packets,
            source_ip_addr=self.source_ip_addr,
            source_mac_addr=self.source_mac_addr,
            source_port=self.source_port,
            destination_ip_addr=self.destination_ip_addr,
            destination_mac_addr=self.destination_mac_addr,
            destination_port=self.destination_port,
            relative_time_gate_seconds=self.relative_time_gate_seconds,
            datetime_gate=self.datetime_gate,
            udp_payload_length_gate=self.udp_payload_length_gate,
        )

    __repr__ = __str__
