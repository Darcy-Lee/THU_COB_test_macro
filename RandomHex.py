import random


class Random4BitGenerator:
    def __init__(self, seed=None):
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    def get_random_4bit(self):
        return format(random.randint(0, 15), 'X')


# 外部调用的封装函数
_generator_instance = None


def initialize_generator(seed=None):
    global _generator_instance
    _generator_instance = Random4BitGenerator(seed)


def get_random_4bit():
    if _generator_instance is None:
        raise ValueError("Generator not initialized. Call initialize_generator(seed) first.")
    return _generator_instance.get_random_4bit()


