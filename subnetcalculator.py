import xlsxwriter
from pprint import pprint

from subnetmanager import SubnetManager as Manager
# from subnetcalculator import SubnetCalculator as Calculator
from utils import Utils

ip = ""
cidr = ""

subnetName = ""
hostsAmount = 0
excelHeader = ["Name", "Hosts Needed", "Hosts Possible", "CIDR", "Networkaddress", "Broadcastaddress",
               "Usable IP Range Start", "Usable IP Range End", "Subnetmask", "Wildcardmask", "Networkaddress Binary",
               "Broadcastaddress Binary", "Usable IP Range Start Binary", "Usable IP Range End Binary",
               "Subnetmask Binary", "Wildcardmask Binary"]

startString = "use \"START\" to start the calculation"
totalAmountLeft = -1

step = 0
while True:
    error = ""
    subnetAmount = Manager.subnet_amount()

    if step == 0:
        print("SubnetCalculator by Mika Schulz")
        network = input("Input a IP/CIDR combination:\n")
        networkSplit = network.split("/")
        if len(networkSplit) == 2:
            ip = networkSplit[0]
            cidr = networkSplit[1]
            if Utils.valid_ip(ip):
                if Utils.valid_cidr(cidr):
                    Manager.create_mother_network(ip, int(cidr))
                    print("Your network supports", Manager.motherNetwork.ipAmount, "IP addresses")
                    step = 1
                else:
                    error = "Invalid CIDR. CIDR must be between 0 and 32. Format: XXX.XXX.XXX.XXX/XX"
            else:
                error = "Invalid Ip. IP parts must be between 0 and 255. Format: XXX.XXX.XXX.XXX/XX"
        else:
            error = "Invalid IP/CIDR combination. Format: XXX.XXX.XXX.XXX/XX"
    if step == 1:
        totalAmountLeft = Manager.possible_ips()
        inputString = ""

        if totalAmountLeft == 0:
            inputString = input("You have used the entire address range. Please " + startString + ":\n")
            if inputString.upper() == "START":
                step = 3
            continue
        elif subnetAmount > 0:
            inputString = input("Enter a subnet name or " + startString + ":\n")
            if inputString.upper() == "START":
                step = 3
                continue
        else:
            inputString = input("Enter a subnet name:\n")
        if inputString.upper() != "START":
            if inputString != "":
                subnetName = inputString
                step = 2
            else:
                error = "You can't name your subnet \"\""
        else:
            error = "You can't name your subnet \"START\""
    if step == 2:
        amountLeft = totalAmountLeft - 2
        maxPossibleSubnetIps = Manager.max_possible_subnet_ips(totalAmountLeft) - 2
        print("You can still use", str(amountLeft), "addresses for clients. Total:", str(totalAmountLeft),
              "[+ 2 (Network- and Broadcastaddress)]")
        print("Maximum usable host ips for this subnet:", maxPossibleSubnetIps)
        hostsAmountString = input("Specify how many hosts \"" + subnetName + "\" should support:\n")
        if hostsAmountString.isdigit():
            hostsAmount = int(hostsAmountString)
            if not hostsAmount <= 0 and not hostsAmount > maxPossibleSubnetIps:
                subnet = Manager.create_subnet(subnetName, hostsAmount)
                subnet.calc_netzworksize()
                step = 1
                continue
            else:
                error = "Invalid hostamount. Amount must be a between 0 and " + str(maxPossibleSubnetIps)
        else:
            error = "Invalid hostamount. Amount must be a positive number"
    if step == 3:
        Manager.subnetList.sort(key=lambda x: (x.cidr, x.name))
        nextFreeIp = Manager.motherNetwork.networkaddress
        for subnet in Manager.subnetList:
            subnet.calc_subnet(nextFreeIp)
            nextFreeIp = subnet.nextFreeIp

        workbook = xlsxwriter.Workbook('Subnetworks.xlsx')
        worksheet = workbook.add_worksheet("Subnetworks")

        worksheet.write_row(0, 0, excelHeader)

        row = 1
        for subnet in Manager.subnetList:
            worksheet.write_row(row, 0, subnet.summary())
            row += 1

        workbook.close()

        print("Your network was exported to \"Subnetworks.xlsx\"!")

        input()
        break
    print("Input error:", error)
