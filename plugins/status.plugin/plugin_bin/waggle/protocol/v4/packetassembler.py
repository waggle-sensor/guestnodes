# ANL:waggle-license
# This file is part of the Waggle Platform.  Please see the file
# LICENSE.waggle.txt for the legal details of the copyright and software
# license.  For more details on the Waggle project, visit:
#          http://www.wa8.gl
# ANL:waggle-license
'''
This module contains a class that assembles packets.
TODO: Handshake to get this going. Ben's paper has the general
idea about the handshake.
'''
from waggle.protocol.PacketHandler import *
from io import StringIO
from collections import deque

class PacketAssembler(object):
	"""
	This class accepts multi-packet messages and reassembles them
	into the original intended message.
	Only ONE PacketAssembler should exist for each node unique ID.
	"""
	MAX_TRANSFERS = 255

	def __init__(self):

		# Prepare to receive on all 255 channels
		self.incoming = [None] * PacketAssembler.MAX_TRANSFERS
		self.completed = deque()


	def reserve_channel(self, num_packets):
		"""
			Tells the PacketAssembler that a new transfer is starting, and
			asks it to get ready to recieve packets on a channel

			:param int num_packets: The number of packets in this transfer
			:rtype: Int - The number of the transfer channel you were given
			:rtype: None - Returned if no channels are available. Try again later!
		"""

		channel = -1
		for reserved in range(0,PacketAssembler.MAX_TRANSFERS):
			if self.incoming[reserved] == None:
				channel = reserved

		# No channels available. Try again later =(
		if channel == -1:
			return None

		# Reservation suceeded.
		self.incoming[channel] = _UnfinishedPacket(num_packets)

		return channel


	def add_packet(self,newPacket):
		"""
			Accepts an incoming packet that is part of a larger file.
			This will write the data to one of the incoming buffers.

			:param string newPacket: A string representing a waggle packet
		"""
		header = get_header(newPacket)
		transfer_num = header["msg_mi_type"]
		self.incoming[transfer_num].add_packet(newPacket)

		# See if the packet is complete.
		if self.incoming[transfer_num].done:
			self.completed.append(self.incoming[transfer_num].getData())
			self.incoming[transfer_num] = None

	def get_complete(self):
		if not self.completed:
			return None
		else:
		 return self.completed.popleft()



class _UnfinishedPacket(object):
	"""
		For internal use.
		This class represents a file in the midst of being assembled
	"""

	# FUTURE IMPROVEMENT: Make it possible to start one of these in a way
	# where the info is written to a file, allowing for large file transfers
	# to not explode everything by eating all the RAM.

	MAX_PACKET_SIZE = 1024

	def __init__(self,numPackets):
		self.info_buffer = StringIO()
		self.num_packets = numPackets
		self.missing_packets = []
		self.last_received = -1
		self.done = False

	def add_packet(self, new_packet):
		"""
			Adds the packet to the unfinished object. Updates all things appropriately

			:param string newPacket: The incoming packet
		"""
		packet = unpack(new_packet)
		reader = StringIO(packet[1]) # Get the actual packet data as a StringIO
		packet_number = _bin_unpack(reader.read(4)) # Read the 4-byte number of the packet

		# Try to write the info to the correct place
		self.info_buffer.seek(_UnfinishedPacket.MAX_PACKET_SIZE * packet_number)
		self.info_buffer.write(reader.read())
		reader.close()
		self.info_buffer.seek(0)
		# Update incoming packet tracking data
		if(packet_number > self.last_received):
			self.last_received = packet_number
			for num in range(self.last_received,packet_number):
				self.missing_packets.append(num)
		else:
			self.missing_packets.remove(packet_number)

		# See if all packets are received.
		if(self.last_received == self.num_packets-1 and not self.missing_packets):
			self.done = True


	def getData(self):
		"""
			If the data is complete, this will return the object.
			Otherwise returns None

			:rtype: String or None
		"""
		if self.done:
			self.info_buffer.seek(0)
			data = self.info_buffer.read()
			self.info_buffer.close()
			return data
		else:
			return None


def _bin_unpack(string):
    """
        For internal module use.
        Takes in a string and returns it in integer format

        :param string string: The binary string to read
        :rtype: int
    """
    x = 0

    for i in range(1, len(string) + 1):
        x = x | (ord(string[-i]) << (i - 1)*8)

    return x
