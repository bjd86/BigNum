import random
import re
import subprocess
import sys

import numpy as np
from BigNumber import BigNumber

NUMBER_SIZE = 30
NUM_TESTS = 1

VERBOSE = 1

def bignum_to_str(my_bignum : BigNumber.BigNumber) -> str:
  """return string representation of BigNumber with
  appropriate number of significant figures"""
  return BigNumber.nstr(BigNumber.to_mpf(my_bignum), NUMBER_SIZE*2)

def sequence_check(bignum0 : BigNumber.BigNumber, bignum1 : BigNumber.BigNumber, num_digits : int) -> bool:
  bignum0_str = bignum_to_str(bignum0)
  bignum1_str = bignum_to_str(bignum1)
  if( len(bignum0_str) < num_digits ):
    bignum0_str = (len(num_digits - bignum0_str))*"0" + bignum0_str
  else:
    bignum0_str = bignum0_str[len(bignum0_str) - num_digits:]

  if( len(bignum1_str) < num_digits ):
    bignum1_str = (len(num_digits - bignum1_str))*"0" + bignum1_str
  else:
    bignum1_str = bignum1_str[len(bignum1_str) - num_digits:]

  
  result = True

  for i in range(num_digits):
    if( bignum0_str[i] != bignum1_str[i] ):
      result = False

  print(f"cpp_BigNum: {bignum0_str} bignum_result: {bignum1_str}")

  return result

def sequence_check2(bignum0 : str, bignum1 : BigNumber.BigNumber, num_digits : int) -> bool:
  # bignum0_str = bignum_to_str(bignum0)
  bignum0_str = str(bignum0)
  bignum1_str = bignum_to_str(bignum1)
  if( len(bignum0_str) < num_digits ):
    bignum0_str = (len(num_digits - bignum0_str))*"0" + bignum0_str
  else:
    bignum0_str = bignum0_str[len(bignum0_str) - num_digits:]

  if( len(bignum1_str) < num_digits ):
    bignum1_str = (len(num_digits - bignum1_str))*"0" + bignum1_str
  else:
    bignum1_str = bignum1_str[len(bignum1_str) - num_digits:]

  
  result = True

  for i in range(num_digits):
    if( bignum0_str[i] != bignum1_str[i] ):
      result = False

  print(f"cpp_BigNum: {bignum0_str} bignum_result: {bignum1_str}")

  return result


method = int(sys.argv[1])
operation = int(sys.argv[2])

print("")

# update_cmd = "make LL AR"
update_cmd = "make AR"

p = subprocess.run(update_cmd, shell=True)

if( p.returncode ):
  print("make failed")
  sys.exit(1)

test_file = './test_nums.txt'

# seed with the current system time
random.seed()

num0 = []
num1 = []

total_failed = 0

with open( test_file, 'w+' ) as f:
  for j in range(NUM_TESTS):
    num0 = []
    num1 = []
    num0_str = ""
    num1_str = ""
    for i in range(0, NUMBER_SIZE, 1):
      num0_digit = random.randint(0, 9)
      num0.append(num0_digit)
      num0_str += str(num0_digit)
      num1_digit = random.randint(0, 9)
      num1.append(num1_digit)
      num1_str += str(num1_digit)

    bignum0 = BigNumber.BigNumber(num0_str)
    bignum1 = BigNumber.BigNumber(num1_str)

    if( operation ):
      print(f"testing {num0_str} - {num1_str}")
    else:
      print(f"testing {num0_str} + {num1_str}")

    bignum_result = bignum0 + bignum1

    # result_test2 = bignum0 + bignum1 + BigNumber.BigNumber("1")
    # print(f"test: {result_test2.value == bignum_result.value}")

    if( method == 0 ):
      if( operation ):
        test_add = f"./AR {num0_str} {num1_str} {NUMBER_SIZE} 1"
      else:
        test_add = f"./AR {num0_str} {num1_str} {NUMBER_SIZE} 0"
    else:
      if( operation ):
        test_add = f"./LL {num0_str} {num1_str} {NUMBER_SIZE} 1"
      else:
        test_add = f"./LL {num0_str} {num1_str} {NUMBER_SIZE} 0"

    if( VERBOSE ):
      print(f"running command: {test_add}\n")

    output = subprocess.run(test_add, capture_output=True, shell=True)

    # print(f"output: {output.stdout}")

    cpp_result = re.findall("(-?\d+)", str(output.stdout))[0]

    if( VERBOSE ):
      print(f"python result : {bignum_to_str(bignum_result)}")
      print(f"returned value: {cpp_result}")

    # trying to avoid using python BigNum because it seems to suck
    if( sequence_check2(cpp_result, bignum_result, NUMBER_SIZE) ):
      print("Pass")
    else:
      print("Fail")
      total_failed += 1

print("\nRESULTS:")

if( total_failed ):
  print(f"Failed {total_failed} out of {NUM_TESTS} tests with number size {NUMBER_SIZE}")
else:
  print(f"Passed {NUM_TESTS} tests with number size {NUMBER_SIZE}")
