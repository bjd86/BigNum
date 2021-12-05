#include <iostream>
#include <cstring>

// AR makes copying easy but append/prepend is difficult

class BigNum {
  private:
    int SIZE;
    short *num;
    bool verbose;
    short SIGN;
  public:
    BigNum( int size, short sign, bool verbose_in ) {
      num = new short[size];
      SIZE = size;
      SIGN = sign;
      verbose = verbose_in;
    }

    BigNum( short* initial_num, int size, short sign, bool verbose_in ) {
      num = new short[size];
      SIZE = size;
      std::memcpy(num, initial_num, sizeof(initial_num[0])*size);
      SIGN = sign;
      verbose = verbose_in;
    }

    void delete_bignum() {
      delete[] num;
    }

    void display(bool new_line) {
      bool found_nonzero = false;
      if (SIGN) {
        std::cout << "-";
      }
      // } else {
      //   std::cout << "+";
      // }
      for( int i = 0; i < SIZE; i++  ) {
        if( verbose || num[i] != 0 || found_nonzero ) {
          std::cout << num[i];
        }
      }
      if( new_line == true ) {
        std::cout << std::endl;
      }
      
      // std::cout << "length: " << get_length() << std::endl;
    }

    int get_length() {
      return SIZE;
    }

    short* get_num() {
      return num;
    }

    short get_num_at( int index ) {
      return num[index];
    }

    void set_num_at( int index, short value ) {
      num[index] = value;
    }

    bool get_verbose() {
      return verbose;
    }

    short get_sign() {
      return SIGN;
    }

    void set_sign( int sign ) {
      SIGN = sign;
    }

};

bool magnitude_bigger( BigNum * bignum0, BigNum *bignum1 ) {
  int i = 0;
  short bignum0_val, bignum1_val;
  for( int i = 0; i < bignum0 -> get_length(); i++ ) {
    bignum0_val = bignum0 -> get_num_at(i);
    bignum1_val = bignum1 -> get_num_at(i);
    if( bignum0_val != bignum1_val ) {
      return bignum0_val > bignum1_val;
    }
  }

  return false;

}

// num0 should be at least as long as bignum1, and should be
// greater in value
BigNum* _subtract( BigNum *bignum0, BigNum *bignum1 ) {
  // std::cout << "Subtract" << std::endl;

  BigNum *difference_bignum = new BigNum(bignum0 -> get_num(), bignum0 -> get_length(), bignum0 -> get_sign(), bignum0 -> get_verbose());

  short prev_dig, num0_cur_val, num1_cur_val;
  int temp_index = 0;

  for ( int i = difference_bignum -> get_length() - 1; i >= 0; i-- ) {
    num0_cur_val = difference_bignum -> get_num_at(i);
    num1_cur_val = bignum1 -> get_num_at(i);
    // std::cout << "i: " << i << " subtracting: " << num0_cur_val << " - " << num1_cur_val;
    // this shouldn't happen when i = 0 bc |bignum0| > |bignum1|
    if( num0_cur_val < num1_cur_val ) {
      temp_index = i - 1;
      prev_dig = difference_bignum -> get_num_at(temp_index);
      while( prev_dig == 0 ) {
        // update this digit to be 9
        difference_bignum -> set_num_at( temp_index, (short)9 );
        temp_index --;
        prev_dig = difference_bignum -> get_num_at(temp_index);
      }
      // subtract 1 from that digit to borrow
      difference_bignum -> set_num_at(temp_index, difference_bignum -> get_num_at(temp_index) - 1);
      num0_cur_val += (short)10;
    }

    difference_bignum -> set_num_at(i, num0_cur_val - num1_cur_val);

    // std::cout << " = " << difference_bignum -> get_num_at(i) << std::endl;

    // difference_bignum -> display(true);

  }

  return difference_bignum;

};

// treats both bignum0 and bignum1 as positives, returns new bignum with sum
BigNum* _add( BigNum *bignum0, BigNum *bignum1 ) {
  // std::cout << "Add" << std::endl;

  short ten = (short)10;

  // don't need to initialize with any values in particular
  BigNum *sum_bignum = new BigNum(bignum0 -> get_length(), 0, bignum0 -> get_verbose());

  short carry = (short)0;
  short sum = (short)0;
  short sum_mod = (short)0;

  for ( int i = bignum0 -> get_length() - 1; i >= 0; i-- ) {
    sum = bignum0 -> get_num_at(i) + bignum1 -> get_num_at(i) + carry;
    sum_mod = sum % ten;
    // std::cout << "adding " << bignum0 -> get_num_at(i) << " + " << bignum1 -> get_num_at(i) << " + " << carry;
    // std::cout << " got sun_mod " << sum_mod;
    carry = (sum >= ten) ? (short)1 : (short)0;
    // std::cout << " got carry " << carry << std::endl;

    sum_bignum -> set_num_at(i, sum_mod);

  }

  return sum_bignum;
}

// subtract 2 bignums, doesn't matter sign or which is bigger
// this is handled by the function
BigNum* subtract( BigNum *bignum0, BigNum *bignum1 ) {
  // cases:
  // both positive: subtract bigger - smaller
  // bignum0 positive, bignum1 negative: add bignum0 + bignum1 as positives, get rid of negative sign
  // bignum0 negative, bignum1 positive: add bignum0 + bignum1 as positives, make result negative
  // bignum0 negative, bignum1 negative:
  //  if( bignum1 > bignum0 ): subtract bignum1 - bignum0 as positives, result is positive
  //  else: subtract bignum0 - bignum1 as positives, result is negative
  BigNum *result;
  // both positive
  if( !bignum0 -> get_sign() && !bignum1 -> get_sign() ) {
    // if bignum0 bigger than bignum1, subtract bignum0 - bignum1
    if( magnitude_bigger( bignum0, bignum1 ) ) {
      result = _subtract(bignum0, bignum1);
      // make sure result is positive
      result -> set_sign( 0 );
    } else {
      result = _subtract(bignum1, bignum0);
      // make sure result is negative
      result -> set_sign( 1 );
    }
  // bignum0 positive, bignum1 negative
  } else if ( !bignum0 -> get_sign() && bignum1 -> get_sign() ) {
    result = _add( bignum0, bignum1 );
    result -> set_sign( 0 );
  // bignum0 negative, bignum1 positive
  } else if ( bignum0 -> get_sign() && !bignum1 -> get_sign() ) {
    result = _add( bignum0, bignum1 );
    result -> set_sign( 1 );
  // bignum0 negative, bignum1 negative
  } else {
    if( magnitude_bigger( bignum0, bignum1 ) ) {
      result = _subtract( bignum0, bignum1 );
      // make sure result is negative
      result -> set_sign( 1 );
    } else {
      result = _subtract( bignum1, bignum0 );
      // make sure result is positive
      result -> set_sign( 0 );
    }
  }

  return result;
  
};

// add 2 bignums, doesn't matter sign or which is bigger
// this is handled by the function
BigNum* add( BigNum *bignum0, BigNum *bignum1 ) {
  // cases:
  // both positive: add both, make positive result
  // bignum0 positive, bignum1 negative: make bignum1 positive, result =  subtract( bignum0, bignum1 )
  // bignum0 negative, bignum1 positive: make bignum0 positive, result =  subtract( bignum1, bignum0 )
  // both negative: add both, make negative result
  BigNum *result;
  // both positive
  if( !bignum0 -> get_sign() && !bignum1 -> get_sign() ) {
    result = _add( bignum0, bignum1 );
    result -> set_sign( 0 );
  } else if ( !bignum0 -> get_sign() && bignum1 -> get_sign() ) {
    // change the sign to positive for the subtraction
    bignum1 -> set_sign( 0 );
    result = subtract( bignum0, bignum1 );
    // change the sign to back to negative
    bignum1 -> set_sign( 1 );
  } else if ( bignum0 -> get_sign() && !bignum1 -> get_sign() ) {
    // change the sign to positive for the subtraction
    bignum0 -> set_sign( 0 );
    result = subtract( bignum1, bignum0 );
    // change the sign to negative for the subtraction
    bignum0 -> set_sign( 1 );
  } else {
    result = _add( bignum0, bignum1 );
	result -> set_sign( 1 );
  }

  return result;
}

int main(int argc, char **argv) {
  int i;

  if( argc < 5 ) {
    std::cout << "Usage is AR bignum1 bignum2 size operation\nopcodes 0:add 1:subtract" << std::endl;
    exit(0);
  }

  // int size = std::stoi(argv[1]);
  int size = std::stoi(argv[3]);

  int operation = std::stoi(argv[4]);

  short *bignum_0 = new short[size];
  short *bignum_1 = new short[size];

  for ( i = 0; i < size; i++ ) {
    bignum_0[i] = (short)(int)argv[1][i] - 48;
    bignum_1[i] = (short)(int)argv[2][i] - 48;
  }

  BigNum *bignum0 = new BigNum(bignum_0, size, 0, true);
  BigNum *bignum1 = new BigNum(bignum_1, size, 0, true);

  // change bignum0 sign
  // bignum0 -> set_sign( 1 );
  // change bignum1 sign
  // bignum1 -> set_sign( 1 );

  // bignum0 -> display(false);
  // bignum1 -> display(false);

  BigNum *result;

  switch(operation) {
    case 0:
      // add the two
      result = add(bignum0, bignum1);
      break;
    case 1:
      // subtract the two
      result = subtract(bignum0, bignum1);
      break;
    default:
      std::cout << "Invalid operation, you entered " << operation << "\ndefaulting to add" << std::endl;
      result = add(bignum0, bignum1);
  }

  result -> display(true);

  bignum0 -> delete_bignum();
  bignum1 -> delete_bignum();
  result  -> delete_bignum();

  delete[] bignum_0;
  delete[] bignum_1;
  delete bignum0;
  delete bignum1;
  delete result;

  return 0;
}
