import sys


class CallableModule(sys.modules[__name__].__class__):
    def __call__(self, *args, **kwargs):
        return self.print_rank_0(*args, **kwargs)

    def print_rank_0(self, *args, **kwargs):
        """Print the message if the rank is 0, otherwise, do nothing."""
        import torch
        if torch.distributed.get_rank() == 0:
            print(*args, **kwargs)


    def print_rank_last(self, *args, **kwargs):
        """Print the message if the current rank is the last one."""
        import torch
        last_rank = torch.distributed.get_world_size() - 1
        if torch.distributed.get_rank() == last_rank:
            print(*args, **kwargs)


# Create an instance of CallableModule
inst = CallableModule(__name__)
inst.__doc__ = inst.print_rank_0.__doc__
sys.modules[__name__] = inst
