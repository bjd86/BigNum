import random
import numpy as np
from BigNumber import BigNumber

test_file = './test_nums.txt'

# seed with the current system time
random.seed()

num0 = num1 = []

with open( test_file, 'w+' ) as f:
  for j in range(200):
    num0 = num1 = []
    num0_str = num1_str = ""
    for i in range(0, 256, 1):
      num0_digit = random.randrange(0, 9, step=1)
      num0.append(num0_digit)
      num0_str += str(num0_digit)
      num1_digit = random.randrange(0, 9, step=1)
      num1.append(num1_digit)
      num1_str += str(num1_digit)

    bignum0 = BigNumber.BigNumber(num0_str)
    bignum1 = BigNumber.BigNumber(num1_str)

    bignum_result = bignum0 + bignum1

    print(bignum_result)
      
    result = list(np.add(num0, num1))
    result = result[-256:]
    # print(f'size result: {len(result)}, size num0: {len(num0)}')
    print(f'{num0}\n{num1}\n{result}\n', file = f)