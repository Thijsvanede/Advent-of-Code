from challenge import Challenge

class ChallengeSolution(Challenge):

    ########################################################################
    #                              Load data                               #
    ########################################################################

    def load(self, path):
        # Load data from path
        with open(path) as infile:
            data = bin(int(infile.read().strip(), 16))[2:]

            # Add padding if necessary
            if len(data) % 8:
                data = '0' * (8 - (len(data) % 8)) + data

        # Return data
        return data

    ########################################################################
    #                              Exercises                               #
    ########################################################################

    def part_1(self, data):
        # Parse packet
        version, type_id, result, data = self.parse(data)

        # Return sum of version numbers
        return version + self.version_sum(result)

    def part_2(self, data):
        # Parse packet
        version, type_id, result, data = self.parse(data)

        # Process packet
        return self.process(version, type_id, result)

    ########################################################################
    #                         Auxiliary functions                          #
    ########################################################################

    def parse(self, data):
        """Parse a packet"""
        # Extract version and type
        version = int(data[0:3], 2)
        type_id = int(data[3:6], 2)

        # Get remainder of packet
        data = data[6:]

        # Extract literal
        if type_id == 4:
            result, data = self.parse_literal(data)
        else:
            # Parse subpacket
            result, data = self.parse_subpacket(data)

        # Return result
        return version, type_id, result, data

    def parse_literal(self, data):
        """Parse a literal"""
        # Initialise result
        result = 0

        # Extract part
        part = int(data[:5], 2)
        data = data[5:]

        # Check if first bit is 1
        while part & 0x10:
            # Add to result
            result = (result << 4) + (part & 0xF)

            # Extract part
            part = int(data[:5], 2)
            data = data[5:]

        # Add to result and return
        return (result << 4) + (part & 0xF), data

    def parse_subpacket(self, data):
        # Extract length_type_id
        length_type_id = int(data[0], 2)
        data           = data[1:]

        # Length in bits
        if length_type_id == 0:
            # Get bitlength
            bit_length = int(data[:15], 2)
            # Get remaining data
            data = data[15:]

            # Extract subpackets and remainder
            subpackets = data[:bit_length]
            data       = data[bit_length:]

            # Get packets
            packets = list()
            while subpackets:
                version, type_id, packet, subpackets = self.parse(subpackets)
                packets.append((version, type_id, packet))

        # Number of subpackets
        else:
            # Get number of subpackets
            subpackets = int(data[:11], 2)
            # Get remaining data
            data = data[11:]

            # Get packets
            packets = list()
            while len(packets) < subpackets:
                version, type_id, packet, data = self.parse(data)
                packets.append((version, type_id, packet))

        # Return result
        return packets, data

    def version_sum(self, data):
        # Initialise result
        result = 0

        # Loop over data
        for version, _, part in data:
            # Add version to result
            result += version

            # Recursively parse part, if necessary
            if isinstance(part, list):
                result += self.version_sum(part)

        # Return result
        return result

    def process(self, version, type_id, data):
        # Sum
        if type_id == 0:
            result = 0
            for part in data:
                result += self.process(*part)

        # Product
        elif type_id == 1:
            result = 1
            for part in data:
                result *= self.process(*part)

        # Minimum
        elif type_id == 2:
            result = float('inf')
            for part in data:
                part = self.process(*part)
                if part < result:
                    result = part

        # Maximum
        elif type_id == 3:
            result = -float('inf')
            for part in data:
                part = self.process(*part)
                if part > result:
                    result = part

        # Literal
        elif type_id == 4:
            result = data

        # Greater than
        elif type_id == 5:
            assert len(data) == 2, "> must be computed on 2 numbers"
            result = int(self.process(*data[0]) > self.process(*data[1]))

        # Less than
        elif type_id == 6:
            assert len(data) == 2, "< must be computed on 2 numbers"
            result = int(self.process(*data[0]) < self.process(*data[1]))

        # Equals
        elif type_id == 7:
            assert len(data) == 2, "== must be computed on 2 numbers"
            result = int(self.process(*data[0]) == self.process(*data[1]))

        else:
            raise NotImplementedError(f"Unknown type_id: {type_id}")

        # Return result
        return result
