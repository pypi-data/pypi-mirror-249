"""
This file contains universal gates in Digital Electronics, NAND and NOR gates. 
"""
class Universal:
    def __init__(self):
        self.nor_output = None
        self.nand_output = None

    def logical_nor(self, input1, input2=None):
        if input2 is None:
            if self.nor_output is None:
                raise ValueError("Circuit connection error")
            else:
                self.nor_output = int(not (input1 or self.nor_output))
        else:
            self.nor_output = int(not (input1 or input2))
        return self.nor_output

    def logical_nand(self, input1, input2=None):
        if input2 is None:
            if self.nand_output is None:
                raise ValueError("Circuit connection error")
            else:
                self.nand_output = int(not (input1 and self.nand_output))
        else:
            self.nand_output = int(not (input1 and input2))
        return self.nand_output
