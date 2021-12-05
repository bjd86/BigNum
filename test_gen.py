import random
import re
import subprocess
import sys
import requests

import numpy as np

class bcolors:
  OK = '\033[92m' #GREEN
  WARNING = '\033[93m' #YELLOW
  FAIL = '\033[91m' #RED
  RESET = '\033[0m' #RESET COLOR

def PASS(message):
  print(f"{bcolors.OK}{message}{bcolors.RESET}")

def FAIL(message):
  print(f"{bcolors.FAIL}{message}{bcolors.RESET}")


NUM_TESTS = 100

VERBOSE = 1

operation_dict = {0 : "plus", 1 : "minus"}

def sequence_check(bignum0 : str, bignum1 : str, num_digits : int) -> bool:
  if( bignum0[0] == "-" ):
    bignum0_sign = "-"
    bignum0_num  = bignum0[1:]
  else:
    bignum0_sign = "+"
    bignum0_num  = bignum0

  if( bignum1[0] == "-" ):
    bignum1_sign = "-"
    bignum1_num  = bignum1[1:]
  else:
    bignum1_sign = "+"
    bignum1_num  = bignum1

  if( len(bignum0_num) < num_digits ):
    bignum0_num = (num_digits - len(bignum0_num))*"0" + bignum0_num
  else:
    bignum0_num = bignum0_num[len(bignum0_num) - num_digits:]

  if( len(bignum1_num) < num_digits ):
    bignum1_num = (num_digits - len(bignum1_num))*"0" + bignum1_num
  else:
    bignum1_num = bignum1_num[len(bignum1_num) - num_digits:]

  
  result = True

  for i in range(num_digits):
    if( bignum0_num[i] != bignum1_num[i] ):
      result = False

  if( bignum0_sign != bignum1_sign ):
    result = False

  print(f"cpp_BigNum: {bignum0} bignum_result: {bignum1}")

  return result


def get_result_web(num0 : str, num1 : str, operation : str) -> str:
  response = requests.get(f"https://www.calculator.net/big-number-calculator.html?cx={num0}&cy={num1}&cp=20&co={operation}")

  pattern = re.compile(".*Result.*break-word;\">(.*)</p><br><form name=\"calc\">.*")
  result = pattern.search(response.text)

  result_w_comma = result.group(1)

  return re.sub(",", "", result_w_comma)

if( __name__ == '__main__' ):
  method = int(sys.argv[1])
  operation_in = int(sys.argv[2])

  operation = operation_dict[operation_in]

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
      NUMBER_SIZE = random.randint(10,100)
      for i in range(0, NUMBER_SIZE, 1):
        num0_digit = random.randint(0, 9)
        num0.append(num0_digit)
        num0_str += str(num0_digit)
        num1_digit = random.randint(0, 9)
        num1.append(num1_digit)
        num1_str += str(num1_digit)

      bignum0 = num0_str
      bignum1 = num1_str

      if( operation == "minus" ):
        print(f"testing {num0_str} - {num1_str}")
      else:
        print(f"testing {num0_str} + {num1_str}")

      bignum_result = get_result_web(num0_str, num1_str, operation)

      # result_test2 = bignum0 + bignum1 + BigNumber.BigNumber("1")
      # print(f"test: {result_test2.value == bignum_result.value}")

      if( method == 0 ):
        if( operation == "minus" ):
          test_add = f"./AR {num0_str} {num1_str} {NUMBER_SIZE} 1"
        else:
          test_add = f"./AR {num0_str} {num1_str} {NUMBER_SIZE} 0"
      else:
        if( operation == "minus" ):
          test_add = f"./LL {num0_str} {num1_str} {NUMBER_SIZE} 1"
        else:
          test_add = f"./LL {num0_str} {num1_str} {NUMBER_SIZE} 0"

      if( VERBOSE ):
        print(f"running command: {test_add}\n")

      output = subprocess.run(test_add, capture_output=True, shell=True)

      # print(f"output: {output.stdout}")

      cpp_result = re.findall("(-?\d+)", str(output.stdout))[0]

      if( VERBOSE ):
        print(f"python result : {bignum_result}")
        print(f"returned value: {cpp_result}")

      # trying to avoid using python BigNum because it seems to suck
      if( sequence_check(cpp_result, bignum_result, NUMBER_SIZE) ):
        PASS("Pass")
      else:
        FAIL("Fail")
        total_failed += 1
        f.write(f"\n{num0_str} {operation} {num1_str} = {cpp_result}\n")
        f.write(f"correct answer: {bignum_result}\n")


  print("\nRESULTS:")

  if( total_failed ):
    FAIL(f"{bcolors.FAIL}Failed{bcolors.RESET} {total_failed} out of {NUM_TESTS} tests with number size {NUMBER_SIZE}")
  else:
    PASS(f"{bcolors.OK}Passed{bcolors.RESET} {NUM_TESTS} tests with number size {NUMBER_SIZE}")
