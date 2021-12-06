import random
import re
import subprocess
import sys
import requests
import argparse

import numpy as np

class bcolors:
  OK = '\033[92m' #GREEN
  WARNING = '\033[93m' #YELLOW
  FAIL = '\033[91m' #RED
  RESET = '\033[0m' #RESET COLOR

def PASS(message):
  print(f"\N{Thumbs Up Sign} {bcolors.OK}{message}{bcolors.RESET}")

def FAIL(message):
  print(f"\N{Police Cars Revolving Light} {bcolors.FAIL}{message}{bcolors.RESET}")

# make this global
VERBOSE = False

operation_list = ["plus", "minus"]

def get_operation(method):
  if( method == "mixed" ):
    operation = operation_list[random.randint(0, len(operation_list)-1)]
  elif( method in operation_list ):
    operation = method
  else:
    FAIL(f"INVAID operation, you selected {method}")
    operation = None
  
  return operation


def get_number_size(selection):
  if( selection == "random" ):
    number_size = random.randint(10, 999)
  else:
    number_size = int(selection)

  return number_size
  

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
  parser = argparse.ArgumentParser(description="Run tests on Big Number calculator, tests generated using www.calculator.net/big-number-calculator.html")
  parser.add_argument('--method', default="AR", type=str, help="LL or AR for cpp BigNumber calculator, defaults to AR")
  parser.add_argument("--operation", default="mixed", type=str, help=f'Type of operation to test, default is mixed, select from {" ".join(operation_list)}')
  parser.add_argument("--number_size", default="random", type=str, help="The size of the numbers you would like to test, keep < 1000")
  parser.add_argument("--num_tests", default=100, type=int, help="Number of tests you would like to run")
  parser.add_argument("--VERBOSE", default=False, type=bool, help="Set the verbosity of the run")
  args = parser.parse_args()

  method = args.method
  operation_in = args.operation
  # make sure we got a valid operation
  if( get_operation(operation_in) == None ):
    sys.exit(1)
  number_size_in = args.number_size 
  num_tests = args.num_tests
  VERBOSE = args.VERBOSE

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
    for j in range(num_tests):
      num0 = []
      num1 = []
      num0_str = ""
      num1_str = ""
      operation = get_operation(operation_in)
      number_size = get_number_size(number_size_in)
      for i in range(0, number_size, 1):
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

      if( method == "AR" ):
        if( operation == "minus" ):
          test_add = f"./AR {num0_str} {num1_str} {number_size} 1"
        else:
          test_add = f"./AR {num0_str} {num1_str} {number_size} 0"
      else:
        if( operation == "minus" ):
          test_add = f"./LL {num0_str} {num1_str} {number_size} 1"
        else:
          test_add = f"./LL {num0_str} {num1_str} {number_size} 0"

      if( VERBOSE ):
        print(f"running command: {test_add}\n")

      output = subprocess.run(test_add, capture_output=True, shell=True)

      # print(f"output: {output.stdout}")

      cpp_result = re.findall("(-?\d+)", str(output.stdout))[0]

      if( VERBOSE ):
        print(f"python result : {bignum_result}")
        print(f"returned value: {cpp_result}")

      # trying to avoid using python BigNum because it seems to suck
      if( sequence_check(cpp_result, bignum_result, number_size) ):
        PASS("Pass")
      else:
        FAIL("Fail")
        total_failed += 1
        f.write(f"\n{num0_str} {operation} {num1_str} = {cpp_result}\n")
        f.write(f"correct answer: {bignum_result}\n")


  print("\nRESULTS:")

  if( total_failed ):
    FAIL(f"{bcolors.FAIL}Failed{bcolors.RESET} {total_failed} out of {num_tests} tests")
  else:
    PASS(f"{bcolors.OK}Passed{bcolors.RESET} {num_tests} tests")
