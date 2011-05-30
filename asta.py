import types
import struct
import datetime

class AstaParamList():
    __HEAD = '$$PACKET_HEADER$$'
    __HEADLEN = len(__HEAD)
    __HEADUNKN1 = 0x0001
    __HEADUNKN2 = 0x0000
    __HEAD1 = 'TAstaParamList'
    __HEAD1LEN = len(__HEAD1)
    __PBEGIN = '$'
    __PARAM = 0x06
    __HEAD1END = 0x01
    __END = 0x00
    __VALUE = 0x0c
    __VALUE_TYPE = 0x02
    __UNKN1 = 0x08
    __UNKN2 = 0x02
    __TYPE_STR = 0x01
    __TYPE_INT = 0x03
    __TYPE_BOOL = 0x05
    __TYPE_TUPLE = 0x0f
    __TYPE_DATE = 0x19
    __DATEDIFF = datetime.date(1899, 12, 30)
    __TYPE = {
        types.StringType: __TYPE_STR,
        types.IntType: __TYPE_INT,
        types.BooleanType: __TYPE_BOOL,
        types.TupleType: __TYPE_TUPLE,
        datetime.date: __TYPE_DATE
        }
    def __type(self, var):
        return self.__TYPE[type(var)]
    def __next_unpack(self, shft, frmt):
        self.__index = self.__index1
        self.__index1 = self.__index + shft
        self.__cur = struct.unpack(frmt, self.ASTA[self.__index:self.__index1])[0]
        return self.__cur
    def __next_str(self, shift):
        return self.__next_unpack(shift, '%ds' % (shift))
    def __next_int(self):
        return self.__next_unpack(4, '<I')
    def __next_be_int(self):
        return self.__next_unpack(4, '>I')
    def __next_byte(self):
        return self.__next_unpack(1, 'B')
    def __init__(self, *args, **kwargs):
        if args:
            self.params = {}
            self.ASTA = args[0]
            self.__index1 = 0
            if self.__next_str(self.__HEADLEN) != self.__HEAD:
                raise ValueError
            if self.__next_be_int() != self.__HEADUNKN1:
                print 'Warning HEADUNKN1'
            if self.__next_be_int() != self.__HEADUNKN2:
                print 'Warning HEADUNKN2'
            DATALEN = self.__next_be_int()
            while self.__next_byte() != self.__END:
                if self.__cur != self.__PARAM:
                    raise ValueError
                PARAMLEN = self.__next_byte()
                PARAM = self.__next_str(PARAMLEN)
                if PARAM[0] == self.__PBEGIN:
                    PARAM = PARAM[1:]
                if self.__next_byte() == self.__HEAD1END and PARAM != self.__HEAD1:
                    raise ValueError
                elif self.__cur == self.__HEAD1END:
                    continue
                if self.__cur != self.__VALUE:
                    raise ValueError
                VALUELEN = self.__next_int()
                VALUE = self.__next_str(VALUELEN)
                if self.__next_byte() != self.__VALUE_TYPE:
                    raise ValueError
                if self.__next_byte() != self.__TYPE_STR:
                    raise ValueError
                if self.__next_byte() != self.__VALUE_TYPE:
                    raise ValueError
                if self.__next_byte() == self.__TYPE_INT:
                    VALUE = int(VALUE)
                if self.__cur == self.__TYPE_BOOL:
                    VALUE = VALUE == 'True'
                if self.__cur == self.__TYPE_DATE:
                    VALUE = self.__DATEDIFF + datetime.timedelta(int(VALUE))
                if self.__next_byte() != self.__UNKN1:
                    print 'Warning UNKN1'
                if self.__next_byte() != self.__UNKN2:
                    print 'Warning UNKN2'
                if self.__next_byte() != self.__END:
                    raise ValueError
                self.params[PARAM] = VALUE
            if (self.__index1 - self.__HEADLEN - 12) != DATALEN:
                print 'Warning DATALEN'
        elif kwargs:
            self.params = kwargs
        else:
            raise ValueError
    def __str__(self):
        DATA = struct.pack(
            '<BB%dsB' % (self.__HEAD1LEN),
            self.__PARAM, self.__HEAD1LEN, self.__HEAD1, self.__HEAD1END
            )
        for param in self.params:
            param1 = self.__PBEGIN + param
            param1len = len(param1)
            value = self.params[param]
            valuetype = self.__type(value)
            if valuetype in (self.__TYPE_INT, self.__TYPE_BOOL):
                value = str(value)
            if valuetype == self.__TYPE_TUPLE:
                value1 = ''
                for elem in value:
                    value1type = self.__type(elem)
                    if value1type == self.__TYPE_INT:
                        value1 = value1 + struct.pack('<I', elem)
                    else:
                        value1 = value1 + elem
                value = value1
            if valuetype == self.__TYPE_DATE:
                value = str((value - self.__DATEDIFF).days)
            valuelen = len(value)
            DATA = DATA + struct.pack(
                '<BB%dsBI%dsBBBBBBB' % (param1len, valuelen),
                self.__PARAM, param1len, param1,
                self.__VALUE, valuelen, value,
                self.__VALUE_TYPE, self.__TYPE_STR, self.__VALUE_TYPE, valuetype,
                self.__UNKN1, self.__UNKN2, self.__END
                )
        DATA = DATA + struct.pack('B', self.__END)
        DATALEN = len(DATA)
        self.ASTA = struct.pack(
            '>%dsIII%ds' % (self.__HEADLEN, DATALEN),
            self.__HEAD, self.__HEADUNKN1, self.__HEADUNKN2, DATALEN, DATA
            )
        return self.ASTA
    def __getitem__(self, key):
        return self.params[key]
