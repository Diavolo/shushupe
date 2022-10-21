from core.utils.my_secrets import RandomSecretKey


class RandomSecretApiKey(RandomSecretKey):
    def __init__(self):
        super().__init__()
