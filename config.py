class Config:
    rows = 6
    col_from_center = 4
    prizes = None
    header_list = list('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!')

    @staticmethod
    def get_columns():
        return Config.col_from_center*2+1

    @staticmethod
    def index(char):
        return Config.header_list.index(char)
