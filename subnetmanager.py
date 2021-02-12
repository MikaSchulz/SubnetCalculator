from subnet import Subnet
from calculator import Calculator as Calculator
from pprint import pprint


class SubnetManager:
    subnetList = []

    motherNetwork = None

    @staticmethod
    def create_mother_network(ip, cidr):
        network = Subnet("Netzwerk", 0)
        network.calc_subnet(ip, cidr)
        SubnetManager.motherNetwork = network
        # pprint(vars(SubnetManager.motherNetwork))
        # print(SubnetManager.motherNetwork)

    @staticmethod
    def create_subnet(name, hosts_amount):
        subnet = Subnet(name, hosts_amount)
        SubnetManager.subnetList.append(subnet)
        return subnet

    @staticmethod
    def possible_ips():
        usedIps = 0
        for subnet in SubnetManager.subnetList:
            usedIps += subnet.ipAmount
        return SubnetManager.motherNetwork.ipAmount - usedIps

    @staticmethod
    def max_possible_subnet_ips(totalAmountLeft):
        x = 1
        while x * 2 <= totalAmountLeft:
            x *= 2
        return x

    @staticmethod
    def subnet_amount():
        amount = len(SubnetManager.subnetList)
        if amount > 0:
            return amount
        return 0
