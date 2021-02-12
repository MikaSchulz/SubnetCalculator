from calculator import Calculator as Calculator


class Subnet:
    # def __init__(self, name, ip, cidr, subnetmask, wildcardmask, networkaddress, broadcastaddress, usableStart,
    #              usableEnd, ipBinary, subnetmaskBinary, wildcardmaskBinary, networkaddressBinary,
    #              broadcastaddressBinary, usableStartBinary, usableEndBinary, ipAmount):
    #     self.name = name
    #     self.ip = ip
    #     self.cidr = cidr
    #     self.subnetmask = subnetmask
    #     self.wildcardmask = wildcardmask
    #     self.networkaddress = networkaddress
    #     self.broadcastaddress = broadcastaddress
    #     self.usableStart = usableStart
    #     self.usableEnd = usableEnd
    #     self.ipBinary = ipBinary
    #     self.subnetmaskBinary = subnetmaskBinary
    #     self.wildcardmaskBinary = wildcardmaskBinary
    #     self.networkaddressBinary = networkaddressBinary
    #     self.broadcastaddressBinary = broadcastaddressBinary
    #     self.usableStartBinary = usableStartBinary
    #     self.usableEndBinary = usableEndBinary
    #     self.ipAmount = ipAmount

    def __init__(self, name, hostsNeeded):
        self.name = name
        self.hostsNeeded = hostsNeeded
        self.ip = ""
        self.cidr = -1
        self.subnetmask = ""
        self.wildcardmask = ""
        self.networkaddress = ""
        self.broadcastaddress = ""
        self.usableStart = ""
        self.usableEnd = ""
        self.ipBinary = ""
        self.subnetmaskBinary = ""
        self.wildcardmaskBinary = ""
        self.networkaddressBinary = ""
        self.broadcastaddressBinary = ""
        self.usableStartBinary = ""
        self.usableEndBinary = ""
        self.ipAmount = -1
        self.nextFreeIp = ""

    def calc_netzworksize(self):
        exp = 1
        ipAmount = 2
        while ipAmount < self.hostsNeeded + 2:
            exp += 1
            ipAmount = pow(2, exp)
        self.ipAmount = ipAmount
        self.cidr = 32 - exp

    def summary(self):
        return [self.name, self.hostsNeeded, self.ipAmount, self.cidr, self.networkaddress, self.broadcastaddress,
                self.usableStart, self.usableEnd, self.subnetmask, self.wildcardmask, self.networkaddressBinary,
                self.broadcastaddressBinary, self.usableStartBinary, self.usableEndBinary, self.subnetmaskBinary,
                self.wildcardmaskBinary]

    def calc_subnet(self, free_ip, cidr=None):

        if cidr is None:
            cidr = self.cidr

        ipBinaryList = []

        subnetmaskBinaryList = []
        wildcardBinaryList = []

        networkaddressBinaryList = []
        broadcastaddressBinaryList = []

        # Adresse zu binär
        ipSplit = free_ip.split(".")
        ipSplitRange = range(0, len(ipSplit))
        for addressPart in ipSplitRange:
            ipBinaryList.extend(list(map(int, Calculator.dec_to_bin(ipSplit[addressPart], 8, False))))

        ipRange = range(0, 32)

        # CIDR in Bits
        for i in ipRange:
            if i < cidr:
                subnetmaskBinaryList.append(1)
                wildcardBinaryList.append(0)
            else:
                subnetmaskBinaryList.append(0)
                wildcardBinaryList.append(1)

        for i in ipRange:
            if ipBinaryList[i] & subnetmaskBinaryList[i]:
                networkaddressBinaryList.append(1)
            else:
                networkaddressBinaryList.append(0)

            if ipBinaryList[i] | wildcardBinaryList[i]:
                broadcastaddressBinaryList.append(1)
            else:
                broadcastaddressBinaryList.append(0)

        self.ip, self.ipBinary = Calculator.bin_list_to_address(ipBinaryList)
        self.cidr = cidr
        self.subnetmask, self.subnetmaskBinary = Calculator.bin_list_to_address(subnetmaskBinaryList)
        self.wildcardmask, self.wildcardmaskBinary = Calculator.bin_list_to_address(wildcardBinaryList)
        self.networkaddress, self.networkaddressBinary = Calculator.bin_list_to_address(networkaddressBinaryList)
        self.broadcastaddress, self.broadcastaddressBinary = Calculator.bin_list_to_address(
            broadcastaddressBinaryList)
        self.usableStart, self.usableStartBinary = Calculator.bin_list_to_address(
            Calculator.calc_address(networkaddressBinaryList, cidr, 1))
        self.usableEnd, self.usableEndBinary = Calculator.bin_list_to_address(
            Calculator.calc_address(broadcastaddressBinaryList, cidr, -1))
        self.ipAmount = Calculator.subnet_ip_amount(wildcardBinaryList)
        self.nextFreeIp = Calculator.bin_list_to_address(
            Calculator.calc_address(broadcastaddressBinaryList, 0, 1))[0]
