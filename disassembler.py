import binascii
import json

ADDR_SIGN = "$"
CONTENT_ADDR_SIGN = "#$"


class Disassembler:
    op_codes_file = 'op_codes.json'
    op_codes = None

    def __init__(self, file):
        self.op_codes
        self.file = file

    @classmethod
    def load_op_codes(cls):
        with open(cls.op_codes_file, 'r') as file:
            # OP_CODE : {size : inst, instruction : str}
            cls.op_codes = json.loads(file.read())


    def load_file(self):
        with open(self.file, 'rb') as file :
            self.raw = file.read()


    def load_hex_instructions(self):
        self.hex = binascii.hexlify(self.raw).decode()
        self.hex = [ '0x' + a + b for a, b in zip(self.hex[::2], self.hex[1::2])]

        self.structure_hex_instructions()

    
    def structure_hex_instructions(self):
        self.hex_instructions = []
        i = 0
        while i < len(self.hex):
            inst_size = self.op_codes[self.hex[i]]['size']
            inst = self.hex[i : i + inst_size]
            inst = inst if isinstance(inst, list) else [inst]
            self.hex_instructions += [inst]
            i = i + inst_size


    def hex_to_assembly(self):
        self.instructions = []
        for hex_inst in self.hex_instructions:
            op_code = self.op_codes[hex_inst[0]]
            inst = op_code['instruction']
            
            if op_code['size'] == 2:
                hex_part = hex_inst[1].replace('0x', '')
            elif op_code['size'] == 3:
                hex_part = hex_inst[2].replace('0x', '') + hex_inst[1].replace('0x', '') 

            if op_code['size'] in [2,3]:
                if 'adr' in inst:
                    inst = inst.replace('adr', ADDR_SIGN + hex_part)
                elif 'D8' in inst:
                    inst =  inst.replace('D8', CONTENT_ADDR_SIGN + hex_part)
                elif 'D16' in inst:
                    inst = inst.replace('D16', CONTENT_ADDR_SIGN + hex_part)
                else:
                    print('INVALID !')
            
            self.instructions += [inst]


if __name__ == '__main__':
    Disassembler.load_op_codes()

    disassemble = Disassembler('space-invaders/invaders.h')

    disassemble.load_file()

    disassemble.load_hex_instructions()

    disassemble.hex_to_assembly()

    for i in disassemble.instructions:
        print(i)
