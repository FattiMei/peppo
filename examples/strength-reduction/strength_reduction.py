from peppo.ir import *


@proc
def mult_by_constant(x, CONST):
    return BinExpr(x, CONST)


if __name__ == '__main__':
    pass
