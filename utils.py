class Utils:

    @staticmethod
    def valid_ip(ip_address):
        if ip_address is None:
            return False
        ip_address_split = ip_address.split(".")
        if len(ip_address_split) != 4:
            return False
        for x in ip_address_split:
            if not x.isdigit():
                return False
            y = int(x)
            if y > 255 or y < 0:
                return False
        return True

    @staticmethod
    def valid_cidr(cidr):
        if cidr is None:
            return False
        if not cidr.isdigit():
            return False
        y = int(cidr)
        if y < 0 or y > 32:
            return False
        return True

    @staticmethod
    def get_col_widths(dataframe):
        # First we find the maximum length of the index columns
        idx_max = [max([len(str(s)) for s in dataframe.index.get_level_values(idx)] + [len(str(idx))]) for idx in
                   dataframe.index.names]
        return idx_max + [max([len(str(s)) for s in dataframe[col].values] + \
                              [len(str(x)) for x in col] if dataframe.columns.nlevels > 1 else [len(str(col))]) for col
                          in dataframe.columns]
