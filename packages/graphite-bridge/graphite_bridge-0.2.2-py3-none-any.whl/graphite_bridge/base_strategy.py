
class BaseStrategy:
    def __init__(self, server_connector):
        self.server_connector = server_connector

    def init(self):
        success = self.server_connector.connect()
        if not success:
            return False
        (success2, config) = self.server_connector.get_client_config()
        if not success2:
            return False
        self.config = config
        return True
    
    def deinit(self):
        return 0

    def on_tick(self):
        print("OnTick")
        return 0
