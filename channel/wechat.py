import itchat
from common.log import logger

import platform
class WechatChannel():
    def __init__(self):
        pass

    def startup(self,method=None):
        if platform.system().lower() == "linux":
            enableCmdQR = 2
        else:
            enableCmdQR = False
        # login by scan QRCode
        if method is None:
            itchat.auto_login(enableCmdQR=enableCmdQR)
        else:
            itchat.auto_login(enableCmdQR=enableCmdQR, loginCallback=method)

        # start message listener
        itchat.run()

    def send(self, msg, receiver):
        logger.info('[WX] sendMsg={}, receiver={}'.format(msg, receiver))
        itchat.send(msg, toUserName=receiver)



