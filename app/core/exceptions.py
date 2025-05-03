class DeconvolutionError(Exception):
    def __init__(self, msg=None):
        self.__msg = msg
