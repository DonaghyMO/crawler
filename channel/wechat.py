import itchat
from common.log import logger


class WechatChannel():
    def __init__(self):
        pass

    def startup(self,method=None):
        # login by scan QRCode
        if method is None:
            itchat.auto_login(enableCmdQR=2)
        else:
            itchat.auto_login(enableCmdQR=2,loginCallback=method)

        # start message listener
        itchat.run()

    def send(self, msg, receiver):
        logger.info('[WX] sendMsg={}, receiver={}'.format(msg, receiver))
        itchat.send(msg, toUserName=receiver)



