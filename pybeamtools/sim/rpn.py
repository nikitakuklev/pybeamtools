#!/usr/bin/env python3
"""Yet Another Reverse Polish Notation calculator.
I hope it doesn't suck too much.
This python script is published under the terms of the WTFPL.
More information on: http://www.wtfpl.net/about/
(Compatible with Python 3.7, 3.8, 3.9, 3.10 & 3.11)
"""
import argparse
import sys
import math
from itertools import chain
import numpy as np

"""
/* define constants and some functions
/* PI
1 atan 4 * sto pi pop
/* log(10)
10 ln sto log_10 pop
/* largest number possible
100 exp sto HUGE pop
HUGE sto on_div_by_zero pop
/* CHange Sign 
udf
chs
-1 *

/* ABSolute value 
udf
abs
0 < pop ? chs : 0 + $

/* MODulo--this one is to confuse the beginner.
udf
mod
= rup swap = rup swap = rup / int rdn * rdn swap - 0 < ? pop rdn + : pop rdn pop $


/* TANgent
udf
tan
= cos swap sin swap /

/* SINe for Degrees
udf
dsin
180 / pi * sin

/* SINe for Degrees
udf
dsin
180 / pi * sin

/* COSine for Degrees
udf
dcos
180 / pi * cos

/* TANgent for Degrees
udf
dtan
180 / pi * tan

/* ArcSINe for Degrees
udf
dasin
asin 180 * pi /

/* ArcCOSine for Degrees
udf
dacos
acos 180 * pi /

/* ArcTANgent for Degrees
udf
datan
atan 180 * pi /

/* RECiprocal
udf
rec
1 swap /

/* Radians TO Degrees
udf
rtod
180 * pi /

/* Degrees TO Radians
udf
dtor
180 / pi *

/* hyperbolic cos
udf
cosh
exp = rec + 2 /

/* hyperbolic sin
udf
sinh
exp = chs rec + 2 /

/* hyperbolic tan
udf
tanh
= sinh swap cosh /

/* inverse hyperbolic cos
udf
acosh
= sqr 1 - sqrt + ln

/* inverse hyperbolic sin
udf
asinh
= sqr 1 + sqrt + ln

/* inverse hyperbolic tan
udf
atanh
= 1 + swap chs 1 + / sqrt ln

/* 10^x 
udf
10x
10 swap pow

/* log base-10
udf
log
ln log_10 /

/* Chebyshev T polynomial
udf
Tn
swap acos * cos

/* hypot function: sqrt(sqr(x)+sqr(y))
udf
hypot
sqr swap sqr + sqrt

/* signal to terminal
udf
beep
1 "\007\n" puts

/* maximum of top two items on stack
udf
max2
< ? swap pop : pop $

/* minimum of top two items on stack
udf
min2
> ? swap pop : pop $

/* maximum of top N items on statck
udf
maxn
sto imaxn pop
< ? swap pop : pop $
imaxn 1 - 1 > ? pop maxn : pop pop $

/* minium of top N items on statck
udf
minn
sto iminn pop
> ? swap pop : pop $
iminn 1 - 1 > ? pop minn : pop pop $

/* show the top of the stack
udf
top
= 1 getformat fprf 1 "\n" puts 

/* duplicate the second-to-top item on the stack
udf
over
rup = rdn swap

/* duplicate top two items on the stack
udf
ddup
rup = rdn swap rup = rdn swap

/* interpolate/extrapolate
/* usage: x x0 x1 y0 y1 interp
udf
interp
swap = rup - rup swap = rup - rdn swap rdn swap / rup - rdn * rdn +

/* compute distance between two (x, y) points
/* usage: x1 y1 x2 y2 dist2
udf
dist2
swap rup - sqr swap rdn - sqr + sqrt

/* rotate stack down N times: N rdnn
udf
rdnn
0 == pop ? pop : 1 - rdn swap rdnn $

/* rotate stack up N times:  N rupn
udf
rupn
0 == pop ? pop : 1 - swap rup rupn $

/* pop top N items from stack: N popn
udf
popn
0 == pop ? pop :
stlv 1 == pop pop ? "error: too few values on stack (popn)\n" 1 puts : swap pop 1 - popn $ $

udf
clr
stlv popn

udf
exit
quit

udf
fact
0.5 + int 1 swap 2 < ? pop pop : pop factloop $

udf
factloop
= rup * rdn 1 - 1 == ? pop pop : pop factloop $

udf
safe_div
0 == ? pop pop pop on_div_by_zero : pop / $

/* (atan(x)+(pi/2))/pi
udf
knee
atan pi 2 / + pi /

/* soft-edge "greater than" function
/* <value> <target> <tolerance> segt
/* = 0 if <value> < <target>
/* grows like ((<value>-<target>)/<tolerance>)^2 otherwise
udf
segt
rup - 0 < ? rdn 3 popn 0 : pop rdn / sqr $

/* soft-edge "less than" function
/* <value> <target> <tolerance> selt
/* = 0 if <value> > <target>
/* grows like ((<value>-<target>)/<tolerance>)^2 otherwise
udf
selt
rup swap rdn segt

/* soft-edge "not equal-to" function
/* <value> <target> <tolerance> sene
/* -> 0 as <value> -> <target> +/- <tolerance>
udf
sene
rup - rdn / 1 > ? - sqr : pop -1 < ? - sqr : pop pop 0 $ $

udf
stepfn
0 < ? pop pop 0 :  == ? pop pop 0.5 : pop pop 1 $ $

udf
true
1 1 ==

udf
false
1 0 ==

/* physical constants
2.99792458e10 sto c_cgs pop
2.99792458e8  sto c_mks pop
4.80325e-10 sto e_cgs pop
1.60217733e-19 sto e_mks pop
9.1093897e-28 sto me_cgs pop
9.1093897e-31 sto me_mks pop
2.81794092e-13 sto re_cgs pop
2.81794092e-15 sto re_mks pop
1.380658e-16 sto kb_cgs pop
1.380658e-23 sto kb_mks pop
0.51099906 sto mev pop
1.0545887e-34 sto hbar_mks pop
6.582173e-22 sto hbar_MeVs pop
1.6726485e-27 sto mp_mks pop
4 pi * 1e-7 * sto mu_o pop
1e7 4 / pi / c_mks sqr / sto eps_o pop

/* constants for alpha-magnets
191.655e-2 sto Kas pop
75.0499e-2 sto Kaq pop

udf
beta.p
= sqr 1 + sqrt /

udf
gamma.p
sqr 1 + sqrt

udf
gamma.beta
sqr 1 swap - sqrt rec

udf
p.beta
= sqr 1 swap - sqrt /

udf
p.gamma
sqr 1 - sqrt


udf
KSprob
sqr -2 * exp sto KSterm
1 sto KSsign
0 sto KSsum
1 sto KSindex
KSloop

udf
KSloop
KSterm KSindex sqr pow
1e-8 < ? cle KSsum 2 *
     : pop KSsign * KSsum + sto KSsum 
       KSindex 1 + sto KSindex
       KSsign -1 * sto KSsign
       cle
       KSloop
     $


/* simple statistics
/* usage: <x1> <x2> <x3> ... <xn> n stats
/* returns mean (top) and standard deviation (top-1)
udf
stats
sto istats sto istatsSave pop 0 sto statsSum sto statsSum2 pop
statsLoop
statsSum istatsSave / 
= sqr statsSum2 istatsSave / - istatsSave * istatsSave 1 - / abs sqrt swap 

udf
statsLoop
0 istats == pop pop ? :
        = statsSum + sto statsSum pop
        sqr statsSum2 + sto statsSum2 pop
        istats 1 - sto istats pop
        statsLoop
        $

/* mean of N values
/* usage: <x1> <x2> <x3> ... <xn> n mean
udf
mean
sto imean sto imeanSave pop 0 sto meanSum pop
meanLoop
meanSum imeanSave /

udf
meanLoop
0 imean == pop pop ? :
        meanSum + sto meanSum pop 
        imean 1 - sto imean pop
        meanLoop
        $

/* rms of N values
/* usage: <x1> <x2> <x3> ... <xn> n rms
udf
rms
sto irms sto irmsSave pop 0 sto rmsSum pop
rmsLoop
rmsSum irmsSave / sqrt

udf
rmsLoop
0 irms == pop pop ? :
        sqr rmsSum + sto rmsSum pop 
        irms 1 - sto irms pop
        rmsLoop
        $

udf
duplog
? true true : false false $

udf
sign
= abs == pop pop ? 1 : -1 $ 0 +


/* mult function so * isn't needed in rpnl commands
udf
mult
*


/* test function prints "true" or "false" based on
/* value on logical stack.  The numerical stack is
/* cleared (!) to prevent rpnl from printing a number
udf
test
? "true\n" : "false\n" $ 1 puts cle


/* compute significance level for two-tailed t distribution:
/* t nu t2SL
udf
t2SL
rup sqr rdn = rup + rdn = rup / rec rdn 2 / 0.5 betai 

/* compute significance level for F-test:
/* var1 var2 nu1 nu2 FSL
udf
FSL
stlv 4 < pop pop ? "usage: <var1> <var2> <nu1> <nu2> FSL\n" 1 puts stop : $
rup rup / 1 < pop ? rec rdn rdn swap : rdn rdn $
ddup 2 / rup 2 / rup 
rup * rdn = rup + rdn swap / 
rdn rdn swap betai

/* compute significance level for Pearson's r (linear correlation coefficient):
/* r nu rSL
udf
rSL
rup abs = sqr 1 - rdn = rup / rec chs sqrt * rdn t2SL

/* compute significance level for chi-squared:
/* chiSq nu Chi2SL
udf
Chi2SL
2 / swap 2 / swap gamQ
"""


class InvalidOperationError(Exception):
    "Invalid operation"

    def __init__(self, message):
        super().__init__(message)
        self.digits = []


class OneDigitError(InvalidOperationError):
    "Invalid operation with a 'one-digit' operation"

    def __init__(self, message, digit=None):
        super().__init__(message)
        self.digits = [digit]


class TwoDigitError(InvalidOperationError):
    "Invalid operation with a 'two-digit' operation"

    def __init__(self, message, digit1=None, digit2=None):
        super().__init__(message)
        self.digits = [digit2, digit1]


def to_float(item):
    return float(item.replace(",", "."))


def is_numeric(item):
    "Return True if the item is numeric"
    try:
        to_float(item)
        return True
    except (ValueError, TypeError):
        pass
    return False


def eval_rpn(s: str) -> float:
    rpn = RPNCalc()
    rpn.push(s)
    if len(rpn.stack) > 1 or len(rpn.stack) == 0:
        raise ValueError(f"Stack {rpn.stack} is incorrect length")
    return rpn.stack[0]


class RPNCalc:
    "Reverse Polish Notation class"

    def __init__(self):
        self.stack = []
        self.substitutions = {}
        self.NO_ITEM_OPS = {
            "drop": self.drop,
            "clear": self.clear,
            "e": self.e,
            "pi": self.pi,
            # "help": self.help,
        }
        self.ONE_ITEM_OPS = {
            "sqrt": self.sqrt,
            "dup": self.dup,
            "floor": self.floor,
            "ceil": self.ceil,
            "abs": self.abs,
            "ln": self.ln,
            "sin": self.sin,
            "cos": self.cos,
            "tan": self.tan,
        }
        self.TWO_ITEM_OPS = {
            "+": self.plus,
            "-": self.minus,
            "*": self.multiply,
            "/": self.divide,
            "^": self.power,
            "**": self.power,
            "pwr": self.power,
            "swap": self.swap,
            "log": self.log,
            "mod": self.mod,
            "%": self.mod,
            "divmod": self.divmod,
        }
        self.THREE_ITEM_OPS = {
            "sene": self.sene,
            "segt": self.segt,
            "selt": self.selt,
        }
        self.ALL_OPS = list(
            chain(
                self.THREE_ITEM_OPS.keys(),
                self.TWO_ITEM_OPS.keys(),
                self.ONE_ITEM_OPS.keys(),
                self.NO_ITEM_OPS.keys(),
            )
        )

    def validate_expression(self, input_buffer: str):
        items = input_buffer.split()
        unknown_tokens = []
        for item in items:
            if is_numeric(item):
                continue
            else:
                if item in self.ALL_OPS:
                    continue
                elif item in self.substitutions:
                    continue
                else:
                    unknown_tokens.append(item)
                    # raise Exception(f'Token {item} unknown')
        return unknown_tokens

    def add_variables(self, kvdict):
        self.substitutions.update(kvdict)

    def handle_op(self, operator):
        """
        Handle any operation known by the calculator.
        """
        # If not in the operators, abort
        if operator not in self.ALL_OPS:
            raise InvalidOperationError(f"Error: `{operator}` unknown")

        if operator in self.NO_ITEM_OPS:
            func = self.NO_ITEM_OPS[operator]
            return func()
        elif operator in self.ONE_ITEM_OPS:
            if len(self.stack) < 1:
                raise InvalidOperationError(f"{operator}: Invalid stack length")
            digit = self.stack.pop()
            func = self.ONE_ITEM_OPS[operator]
            return func(digit)
        elif operator in self.TWO_ITEM_OPS:
            if len(self.stack) < 2:
                raise InvalidOperationError(f"{operator}: Invalid stack length")
            digit1, digit2 = self.stack.pop(), self.stack.pop()
            func = self.TWO_ITEM_OPS[operator]
            return func(digit1, digit2)
        elif operator in self.THREE_ITEM_OPS:
            if len(self.stack) < 3:
                raise InvalidOperationError(f"{operator}: Invalid stack length")
            digit1, digit2, digit3 = (
                self.stack.pop(),
                self.stack.pop(),
                self.stack.pop(),
            )
            func = self.THREE_ITEM_OPS[operator]
            return func(digit1, digit2, digit3)

    # -- Stack operations
    def push(self, input_buffer):
        "Push items in the stack and process them if they're operators"
        result = []
        items = input_buffer.split()
        for item in items:
            try:
                if is_numeric(item):
                    self.stack.append(to_float(item))
                elif item in self.substitutions:
                    self.stack.append(self.substitutions[item])
                else:
                    result = self.handle_op(item)
            except InvalidOperationError as msg:
                print(msg)
                # catch digits back
                if msg.digits:
                    self.stack.extend(msg.digits)

            while result:
                self.stack.append(result.pop())

    def drop(self):
        "Drop the last inserted item out of the stack"
        if not self.stack:
            raise InvalidOperationError("drop: Invalid stack length")
        # drop the "drop" command
        self.stack.pop()

    def clear(self):
        "Clear the stack"
        self.stack = []

    def swap(self, digit1, digit2):
        "Swap the last two items in the stack"
        return [digit2, digit1]

    def dup(self, digit1):
        "Duplicates the last item in the stack"
        return [digit1, digit1]

    def get_status(self):
        "Return the last item in the stack (should be a digit)"
        if self.stack:
            return str(self.stack[-1])
        return "The stack is empty."

    # 3 OP
    def sene(self, T, V2, V1):
        # val, target, tol in reverse
        if np.abs(V1 - V2) < T:
            return [0.0]
        else:
            if V1 > V2:
                return [pow(((V1 - (V2 + T)) / T), 2)]
            elif V2 > V1:
                return [pow(((V2 - (V1 + T)) / T), 2)]
            else:
                return [0.0]

    def segt(self, T, V2, V1):
        if V1 > V2:
            return [pow((V1 - V2) / T, 2)]
        else:
            return [0.0]

    def selt(self, T, V2, V1):
        if V1 < V2:
            return [pow((V1 - V2) / T, 2)]
        else:
            return [0.0]

    # -- Math operators
    def plus(self, digit1, digit2):
        "Add two digits"
        return [digit1 + digit2]

    def minus(self, digit1, digit2):
        "Substract two digits"
        return [digit2 - digit1]

    def multiply(self, digit1, digit2):
        "Multiply two digits"
        return [digit1 * digit2]

    def divide(self, digit1, digit2):
        "Divide two digits"
        try:
            return [digit2 / digit1]
        except ZeroDivisionError:
            raise TwoDigitError(
                "divide: Division by Zero", digit1=digit1, digit2=digit2
            )

    def e(self):
        "Put 'e' constant in the stack"
        return [math.e]

    def pi(self):
        "Put 'pi' constant in the stack"
        return [math.pi]

    def sqrt(self, digit):
        "Extract the square root of the digit"
        try:
            return [math.sqrt(digit)]
        except ValueError as e:
            raise OneDigitError(f"sqrt: {e}", digit)

    def floor(self, digit):
        "Rounding down the digit"
        return [math.floor(digit)]

    def ceil(self, digit):
        "Rounding up the digit"
        return [math.ceil(digit)]

    def abs(self, digit):
        "Absolute value of the digit"
        return [math.fabs(digit)]

    def ln(self, digit):
        "Natural logarithm"
        try:
            return [math.log(digit)]
        except ValueError as e:
            raise OneDigitError(f"ln: {e}", digit)

    def log(self, digit1, digit2):
        "N-based logarithm"
        try:
            return [math.log(digit2, digit1)]
        except (ValueError, ZeroDivisionError) as e:
            raise TwoDigitError(f"ln: {e}", digit1, digit2)

    def power(self, digit1, digit2):
        "Raise the digit2 to the power of the digit1"
        return [digit2**digit1]

    def mod(self, digit1, digit2):
        "Remainder of the division"
        return [digit2 % digit1]

    def divmod(self, digit1, digit2):
        "Quotient and remainder"
        quotient = self.divide(digit1, digit2).pop()
        quotient = float(int(quotient))
        remainder = self.mod(digit1, digit2).pop()
        return [remainder, quotient]

    def sin(self, digit1):
        "Sinus"
        return [math.sin(digit1)]

    def cos(self, digit1):
        "Cosinus"
        return [math.cos(digit1)]

    def tan(self, digit1):
        "Tangent"
        return [math.tan(digit1)]
