# %%
import logging
from pathlib import Path
from typing import Union

from pytars.readers.pcap.pcap_filters import PcapPacketFilters
from pytars.readers.pcap.pcap_headers import (
    Ethernet2Header,
    GlobalHeader,
    IPv4Header,
    PacketHeader,
    PcapPacket,
    PTPv2,
    UDPData,
    UDPHeader,
    VLANHeader,
)


def get_file_size_total_bytes(file_name: Union[Path, str]) -> int:
    """Get the total number of bytes in a file."""
    with open(file_name, "rb") as file:
        # get current location in file
        file.seek(0, 2)  # Move the pointer to the end of the file
        file_size = file.tell()  # Get the position, which is the size of the file in bytes
    return file_size


class PcapReader:
    """A class to read a pcap file."""

    def __init__(self, file_name: Union[Path, str], packet_filters: PcapPacketFilters):
        self.file_name = file_name
        self.total_file_bytes = get_file_size_total_bytes(file_name)
        self.filters = packet_filters
        self.file_handle = None
        self.first_packet_timestamp = None
        self.num_bytes_read = 0
        self.current_packet_num = 0

    def __enter__(self):
        """Enter to be used with 'with' statement."""
        logging.info(f"Opening pcap file: {self.file_name}")
        self.file_handle = open(self.file_name, "rb")
        self.global_header = GlobalHeader(self.file_handle.read(24))
        if self.global_header.magic_number != 0xA1B2C3D4:
            logging.error(f"Invalid magic number in pcap file: {self.global_header.magic_number}")
            raise ValueError("Invalid magic number in pcap file.")
        self.num_bytes_read = 24
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit to be used with 'with' statement."""
        if self.file_handle:
            self.file_handle.close()
            logging.info("Closing pcap file.")

    def __iter__(self):
        return self

    def __next__(self) -> PcapPacket:
        while True:
            # Check if we exceed the max number of packets to read
            if (
                self.filters.max_packets is not None
                and self.current_packet_num >= self.filters.max_packets
            ):
                raise StopIteration

            # check if we're at end of file
            if self.num_bytes_read >= self.total_file_bytes:
                raise StopIteration

            # Read the next packet
            packet = self.read_next_packet()
            self.current_packet_num += 1

            # Check if we have reached a filter that would stop file reading
            if not self.passes_stop_filters(packet):
                logging.debug("Stopping Iteration")
                raise StopIteration

            # Check if the packet passes the continue filters - if not, read the next packet
            if self.passes_continue_filters(packet):
                break

        # return the packet
        return packet

    def read_next_packet(self) -> PcapPacket:
        packet = PcapPacket(packet_ind=self.current_packet_num)

        # Read the packet header
        packet.packet_header = PacketHeader(self.file_handle.read(16), self.first_packet_timestamp)
        self.num_bytes_read += 16
        if not self.first_packet_timestamp:
            self.first_packet_timestamp = packet.packet_header.timestamp_seconds
            packet.packet_header.relative_timestamp_seconds = 0

        # read remaining packet data
        packet_data = self.file_handle.read(packet.packet_header.capture_length)
        self.num_bytes_read += packet.packet_header.capture_length

        # read ethernet header
        packet.ethernet_header = Ethernet2Header(packet_data[:14])
        packet_data = packet_data[14:]

        # read vlan header
        if packet.ethernet_header.is_vlan:
            packet.vlan_header = VLANHeader(packet_data[:4])
            packet_data = packet_data[4:]

        # read ipv4 header
        if packet.ethernet_header.is_ipv4 or (
            packet.vlan_header is not None and packet.vlan_header.is_ipv4
        ):
            packet.ipv4_header = IPv4Header(packet_data)
            ind_start = packet.ipv4_header.header_length * 4
            packet_data = packet_data[ind_start:]

            # read udp header
            if packet.ipv4_header.is_udp:
                packet.udp_header = UDPHeader(packet_data[:8])
                if packet.udp_header.destination_port == 319:  # assumes ptp is on port 319
                    packet.ptpv2 = PTPv2(packet_data[8:])
                packet.udp_data = UDPData(packet_data[8:])

        return packet

    def passes_continue_filters(self, packet):
        # check time gate
        if self.filters.relative_time_gate_seconds is not None:
            if (
                packet.packet_header.relative_timestamp_seconds
                < self.filters.relative_time_gate_seconds[0]
            ):
                logging.log(5, f"Packet {packet.packet_ind} failed relative time gate [low].")
                logging.log(
                    5, f"  relative time: {packet.packet_header.relative_timestamp_seconds}"
                )
                logging.log(5, f"  time gate: {self.filters.relative_time_gate_seconds}")
                return False

        # check source ip address
        if self.filters.source_ip_addr is not None and packet.ipv4_header is not None:
            if packet.ipv4_header.source_ip_address_str != self.filters.source_ip_addr:
                logging.log(5, f"Packet {packet.packet_ind} failed source ip check.")
                logging.log(5, f"  source ip: {packet.ipv4_header.source_ip_address_str}")
                logging.log(5, f"  source ip filter: {self.filters.source_ip_addr}")
                return False

        # check source mac address
        if self.filters.source_mac_addr is not None and packet.ethernet_header is not None:
            if packet.ethernet_header.source_mac_addr != self.filters.source_mac_addr:
                logging.log(5, f"Packet {packet.packet_ind} failed source mac check.")
                logging.log(5, f"  source mac: {packet.ethernet_header.source_mac_addr}")
                logging.log(5, f"  source mac filter: {self.filters.source_mac_addr}")
                return False

        # check source port
        if self.filters.source_port is not None and packet.udp_header is not None:
            if packet.udp_header.source_port != self.filters.source_port:
                logging.log(5, f"Packet {packet.packet_ind} failed source port check.")
                logging.log(5, f"  source port: {packet.udp_header.source_port}")
                logging.log(5, f"  source port filter: {self.filters.source_port}")
                return False

        # check destination ip address
        if self.filters.destination_ip_addr is not None and packet.ipv4_header is not None:
            if packet.ipv4_header.destination_ip_addr != self.filters.destination_ip_addr:
                logging.log(5, f"Packet {packet.packet_ind} failed destination ip check.")
                logging.log(5, f"  destination ip: {packet.ipv4_header.destination_ip_addr}")
                logging.log(5, f"  destination ip filter: {self.filters.destination_ip_addr}")
                return False

        # check destination mac address
        if self.filters.destination_mac_addr is not None and packet.ethernet_header is not None:
            if packet.ethernet_header.destination_mac_addr != self.filters.destination_mac_addr:
                logging.log(5, f"Packet {packet.packet_ind} failed destination mac check.")
                logging.log(5, f"  destination mac: {packet.ethernet_header.destination_mac_addr}")
                logging.log(5, f"  destination mac filter: {self.filters.destination_mac_addr}")
                return False

        # check destination port
        if self.filters.destination_port is not None and packet.udp_header is not None:
            if packet.udp_header.destination_port != self.filters.destination_port:
                logging.log(5, f"Packet {packet.packet_ind} failed destination port check.")
                logging.log(5, f"  destination port: {packet.udp_header.destination_port}")
                logging.log(5, f"  destination port filter: {self.filters.destination_port}")
                return False

        # check datetime gate
        if self.filters.datetime_gate is not None:
            if packet.packet_header.datetime < self.filters.datetime_gate[0]:
                logging.log(5, f"Packet {packet.packet_ind} failed datetime check.")
                logging.log(5, f"  datetime: {packet.packet_header.datetime}")
                logging.log(5, f"  datetime filter: {self.filters.datetime_gate}")
                return False

        # check udp payload bytes gate
        if packet.udp_header is None:
            return False
        elif self.filters.udp_payload_length_gate is not None:
            if (packet.udp_header.length < (self.filters.udp_payload_length_gate[0] + 8)) or (
                packet.udp_header.length > (self.filters.udp_payload_length_gate[1] + 8)
            ):
                logging.log(5, f"Packet {packet.packet_ind} failed udp payload bytes check.")
                logging.log(5, f"  udp payload bytes: {packet.udp_header.length}")
                logging.log(
                    5, f"  udp payload bytes filter: {self.filters.udp_payload_length_gate}"
                )
                return False

        return True  # Replace with actual checking logic

    def passes_stop_filters(self, packet):
        # check relative time gate
        if self.filters.relative_time_gate_seconds is not None and packet.udp_header is not None:
            if (
                packet.packet_header.relative_timestamp_seconds
                > self.filters.relative_time_gate_seconds[1]
            ):
                logging.debug(f"Packet {packet.packet_ind} failed relative time gate check [high].")
                logging.debug(f"  relative time: {packet.packet_header.relative_timestamp_seconds}")
                logging.debug(f"  time gate: {self.filters.relative_time_gate_seconds}")
                return False

        return True  # Replace with actual checking logic
