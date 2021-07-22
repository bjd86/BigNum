import sys
import re

bignum0 = sys.argv[1]
bignum1 = sys.argv[2]

print( f'bignum0: {bignum0}\nbignum1: {bignum1}' )

bignum0 = [x for x in bignum0]
bignum1 = [x for x in bignum1]

if( bignum0[0] == '-' or bignum1[0] == '-' ):
  if( bignum0[0] != bignum1[0] ):
    print('NOT EQUAL')
    sys.exit(0)

bignum0 = bignum0[1:] if re.match('[-+]+', bignum0[0]) else bignum0
bignum1 = bignum1[1:] if re.match('[-+]+', bignum1[0]) else bignum1

bignum0 = [x for x in bignum0 if not re.match(',', x)]
bignum1 = [x for x in bignum1 if not re.match(',', x)]

if( len(bignum0) != len(bignum1) ):
  print('NOT EQUAL')
  sys.exit(0)

for i in range(len(bignum0)):
  if( bignum0[i] != bignum1[i] ):
    print('NOT EQUAL')
    sys.exit(0)

print('EQUAL')