from peppo.ir import *


DIGIT_POW_LUT = [d**d if d > 0 else 0 for d in range(10)]


@proc
def read_digit_pow(digit):
    # a possible scheduling decision could be the
    # placement of this constant in the memory hierarchy
    lut = Constant(DIGIT_POW_LUT, name='lut')

    return MemRef(lut, digit)


@proc
def read_digit_pow_branchless(digit):
    # this is not a procedure! Recursion is carried to the end
    def recursive_helper(ir, i):
        if i == 10:
            return ir
        else:
            return recursive_helper(
                # I'll let LLVM lower the `select` instruction for the given target
                Select(Eq(ir,i), DIGIT_POW_LUT[i], 0),
                i+1)

    return recursive_helper(digit, 0)


# this function makes assumptions on the type of the input
# in the future they will be encoded in type hints
@proc
def fast_digit_pow(digit, exp, BITS):
    @proc
    def fast_digit_pow_tail(digit, exp, i, squares, acc):
        lsb = And(exp, 1)

        return If(
            Lt(i, BITS),
            fast_pow_tail(
                digit,
                Shr(exp,1),
                Add(i,1),
                Mul(squares,squares),
                Select(lsb, Add(acc, squares), acc)),
            acc)

    return fast_pow_tail(digit, exp, 0, digit, 0)


if __name__ == '__main__':
    pass


