import sys


def print_rank_0(self, *args, **kwargs):
    """Print only on rank 0."""
    import torch
    if torch.distributed.get_rank() == 0:
        print(*args, **kwargs)


def print_rank_last(self, *args, **kwargs):
    """Print only on last rank."""
    import torch
    last_rank = torch.distributed.get_world_size() - 1
    if torch.distributed.get_rank() == last_rank:
        print(*args, **kwargs)


class CallableModule(sys.modules[__name__].__class__):
    def __call__(self, *args, **kwargs):
        return self.print_rank_0(*args, **kwargs)


sys.modules[__name__].__class__ = CallableModule
