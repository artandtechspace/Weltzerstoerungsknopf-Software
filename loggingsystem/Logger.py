
# TODO
class Logger:

    def __init__(self, name: str):
        self.name = name

    def debug(self, method: str, message: any):
        print("\t[DBG] ("+self.name+"/"+method+") "+str(message))

    def error(self, method: str, message: any):
        print("[ERROR] ("+self.name+"/"+method+") "+str(message))
        pass

    def warn(self, method: str, message: any):
        print("[WARNING] ("+self.name+"/"+method+") "+str(message))
        pass