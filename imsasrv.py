import SocketServer
import sys
import datetime
import kinterbasdb
from asta import AstaParamList

class IMSAsrv(SocketServer.BaseRequestHandler):

    __ERR = str(AstaParamList(Result = False))

    def __query(self, cursor, sql):
        cursor.execute(sql)
        return cursor.fetchone()[0]

    def handle(self):
        print datetime.datetime.now(), self.client_address[0]
        try:
            self.data = AstaParamList(self.request.recv(1024))
            con = kinterbasdb.connect(dsn = self.data['DataBase'],
                user = self.data['UserName'], password = self.data['Password'],
                charset = 'WIN1251')
            cur = con.cursor()
            ServerDate = self.__query(cur, "select cast('now' as date) as SrvDate from rdb$database")
            if self.__query(cur, "select VALUE_STR from SYSTEM_VARIABLE where NAME = 'PROJECT_CODE'") != self.data['ProjectCode']:
                raise Exception, 'Project code is not valid'
            DepID = self.__query(cur, "select depid from getconst")
            UnKnown = self.__query(cur, "select VALUE_STR from SYSTEM_VARIABLE where NAME = 'UPDATE_DOWNLOAD_PATH'")
            con.close()
            licfile = open('personal.lic')
            lic = licfile.read()
            licfile.close()
            serfile = open('serial.txt')
            serial = serfile.readline().strip()
            serfile.close()
            liclen = len(lic)
            self.request.send(str(AstaParamList(Result = True,
                LicenseTransportVersion = 'VR02', LicenseSerials = serial,
                LicenseDepID = DepID, LicenseServerDate = ServerDate,
                LicenseStream0 = (liclen, device, lic), LicenseCount = 1)))
        except Exception as e:
            print datetime.datetime.now(), e
            self.request.send(self.__ERR)

if __name__ == '__main__':
    try:
        device = sys.argv[1]
    except:
        device = 'F:\\'
    HOST, PORT = '', 3127
    server = SocketServer.TCPServer((HOST, PORT), IMSAsrv)
    while True:
        try:
            print '%s started' % datetime.datetime.now()
            server.serve_forever()
        except KeyboardInterrupt:
            break
        finally:
            print '%s stoped' % datetime.datetime.now()
