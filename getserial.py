import socket
import string
import getpass
from asta import AstaParamList

def main():
    dhost = 'server'
    dbase = 'c:\\ib\\arbit\\arbit.gdb'
    duser = 'SYSDBA'
    dpass = 'masterkey'

    HOST = raw_input('Server [%s]: ' % dhost)
    if not HOST: HOST = dhost
    BASE = raw_input('Database [%s]: ' % dbase)
    if not BASE: BASE = dbase
    USER = raw_input('User [%s]: ' % duser)
    if not USER: USER = duser
    PASS = getpass.getpass('Password [%s]: ' % dpass)
    if not PASS: PASS = dpass
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, 3127))
    s.send(str(AstaParamList(Command = 'GET_LICENSE_DATA', ProjectCode = 'DILO1',
        DataBase = string.join((HOST, BASE), ':'), UserName = string.upper(USER),
        Password = PASS)))
    SERIAL = AstaParamList(s.recv(1024))['LicenseSerials']
    s.close()
    print '\n%s\n' % SERIAL
    f = open('serial.txt', 'w+')
    f.write(SERIAL)
    f.close()

if __name__ == '__main__':
    main()
