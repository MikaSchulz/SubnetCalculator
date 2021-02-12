class Calculator:
    ipRange = range(0, 32)

    @staticmethod
    def full_adder(inputA, inputB, inputC):
        outputSum = inputA ^ (inputB ^ inputC)
        outputCarry = ((inputA ^ inputB) & inputC) | (inputA & inputB)
        return outputSum, outputCarry

    @staticmethod
    def conv_dec_to_same_bin_bit(first, second):
        if abs(first) < abs(second):
            temp = first
            first = second
            second = temp
        first_result = Calculator.dec_to_bin(first, 0, True)
        second_result = Calculator.dec_to_bin(second, len(first_result) - 1, True)
        return first_result, second_result

    @staticmethod
    def calc(first_string, second_string):
        first = list(map(int, first_string))
        second = list(map(int, second_string))
        summ = ""
        x = len(first) - 1
        tempSum = 0
        carry = 0
        while x >= 0:
            # print(first[x], second[x], carry)
            tempSum, carry = Calculator.full_adder(first[x], second[x], carry)
            # print(tempSum, carry)
            summ += str(tempSum)
            x -= 1
        # print(first[0], second[0], carry)
        sumExt, carryExt = Calculator.full_adder(first[0], second[0], carry)
        if sumExt != tempSum:
            summ += str(sumExt)
            # print(tempSum, carry)
        return summ[::-1]

    # Umrechnen von Dezimalzahlen in Binärzahlen
    @staticmethod
    def dec_to_bin(dec_string, bits, twos_compl):
        decimal = int(dec_string)
        if bits != 0:
            max_num = pow(2, bits) - 1
            if decimal > max_num:
                return "Maximum value is exceeded: " + str(max_num)
        negative = False
        if decimal < 0:
            decimal = abs(decimal)
            negative = True
        # print(decimal)
        # print(negative)
        binary_string = ""
        while decimal > 0:
            binary = decimal % 2
            binary_string += str(binary)
            decimal = decimal // 2
        binary_string = (bits * "0" + binary_string[::-1])[-bits:]
        # print("binary_string", str(binary_string))
        # print("twos_compl", str(twos_compl))
        if twos_compl:
            binary_string = "0" + binary_string
            # print("binary_string", str(binary_string))
            if negative:
                # print("negative", str(negative))
                negativeBinary = ""
                for x in binary_string:
                    negativeBinary += str(int(x) ^ 1)
                # print("negativeBinary", negativeBinary)
                negativeBinary = Calculator.calc(negativeBinary,
                                                 Calculator.dec_to_bin("1", len(negativeBinary) - 1, True))
                # print("negativeBinary", negativeBinary)
                return negativeBinary
        return binary_string

    # Umrechnen von Binärzahlen (8 Bit) in Dezimalzahlen
    @staticmethod
    def bin_to_dec(binary, twos_compl):
        x = len(binary) - 1
        decimal = 0
        step = 1
        while x >= 0:
            # print("decimal", decimal)
            # print("binary[x]", binary[x])
            # print("next", int(binary[x]) * step * (1 if not twos_compl or x != 0 else -1))
            decimal += int(binary[x]) * step * (1 if not twos_compl or x != 0 else -1)
            # print("decimal", decimal)
            # print("step", step)
            step = step * 2
            # print("step", step)
            x -= 1
        return str(decimal)

    @staticmethod
    def subnet_ip_amount(wildcardBinaryList):
        binary = ""
        for x in wildcardBinaryList:
            if x == 1:
                binary += str(x)
        return int(Calculator.bin_to_dec(binary, False)) + 1

    # Umrechnung einer binären Liste zu einer binären und dezimalen Adresse
    @staticmethod
    def bin_list_to_address(binary_list):
        decimal_address = ""
        binary_address = ""
        part = ""
        for x in Calculator.ipRange:
            # subnetmask += str(subnetmaskBinaryList[bit])
            part += str(binary_list[x])
            if (x + 1) % 8 == 0:
                # print(part)
                decimal_address += Calculator.bin_to_dec(part, False)
                binary_address += part
                # print(subnetmask)
                part = ""
                if x + 1 != Calculator.ipRange.stop:
                    decimal_address += "."
                    binary_address += "."
        return decimal_address, binary_address

    @staticmethod
    def calc_address(addressBinaryList, cidr_count, add):
        addressBinList = addressBinaryList.copy()
        host_part = "0" + "".join(str(x) for x in addressBinList[cidr_count:])
        to_add = Calculator.dec_to_bin(str(add), len(host_part) - 1, True)
        host_part = Calculator.calc(host_part, to_add)[1:]

        for x in range(cidr_count, len(addressBinList)):
            addressBinList[x] = int(host_part[x - cidr_count])
        return addressBinList
