#include <iostream>

class Digit {
  public:
    Digit *next_digit, *prev_digit;
    short value;
    Digit( Digit *next, Digit *last, short val ) {
      next_digit = next;
      prev_digit = last;
      value = val;
    }
};

class BigNum {
  private:
    int len_num;
    Digit *last_digit;
  public:
    Digit *num;
    BigNum() {
      num = NULL;
      last_digit = NULL;
      len_num = 0;
    }
    
    BigNum( short* initial_num, int size ) {
      num = NULL;
      last_digit = NULL;
      len_num = 0;
      for( int i = 0; i < size; i++) {
        append_num(initial_num[i]);
      }
    }

    void append_num( short new_val ) {
      Digit* new_digit = new Digit(NULL, NULL, new_val);
      // degenerate case, no numbers yet
      if( last_digit == NULL ) {
        num = last_digit = new_digit;
      } else {
        new_digit -> prev_digit = last_digit;
        last_digit -> next_digit = new_digit;
        last_digit = new_digit;
      }
      len_num += 1;
    }

    void prepend_num( short new_val ) {
      Digit* new_digit = new Digit(NULL, NULL, new_val);
      // degenerate case, no numbers yet
      if( last_digit == NULL ) {
        num = last_digit = new_digit;
      } else {
        new_digit -> next_digit = num;
        num -> prev_digit = new_digit;
        num = new_digit;
      }
      len_num += 1;
    }

    void remove_last_num() {
      if( last_digit != NULL ) {
        Digit *new_last = last_digit -> prev_digit;
        delete last_digit;
        new_last -> next_digit = NULL;
        len_num -= 1;
        last_digit = new_last;
      } else {
        std::cout << "You are trying to remove from an empty number" << std::endl;
      }
    }

    void delete_bignum() {
      if( last_digit != NULL ) {
        for( int i = 0; i < len_num; i++ ) {
          remove_last_num();
        }
      } else {
        std::cout << "You are trying to remove from an empty number" << std::endl;
      }
    }

    void display() {
      Digit *cur_num = num;
      while( cur_num != NULL ) {
        std::cout << cur_num -> value;
        cur_num = cur_num -> next_digit;
      }
      std::cout << std::endl;
      std::cout << "current length: " << get_length() << std::endl;
    }

    int get_length() {
      return len_num;
    }

    void add( BigNum bignum1 ) {

    }

    // does not assume both numbers are the same length,
    // that would simplify a bit
    // takes two positives right now
    void _add( BigNum bignum1 ) {
      std::cout << "Add" << std::endl;
      Digit *num0_cur = last_digit;
      Digit *num1_cur = bignum1.last_digit;

      short num0_cur_val, num1_cur_val, carry = 0, sum, sum_mod;

      bool num0_null = num0_cur == NULL;
      bool num1_null = num1_cur == NULL;

      while( !num0_null || !num1_null ) {
        num0_cur_val = (num0_null) ? 0 : num0_cur -> value;
        num1_cur_val = (num1_null) ? 0 : num1_cur -> value;
        sum = num0_cur_val + num1_cur_val + carry;
        sum_mod = sum % 10;
        carry = (sum >= 10) ? 1 : 0;

        if( num0_null ) {
          prepend_num(sum_mod);
          num0_cur = NULL;
        } else {
          num0_cur -> value = sum_mod;
          num0_cur = num0_cur -> prev_digit;
        }

        num1_cur = (num1_null) ? NULL : num1_cur -> prev_digit;

        num0_null = num0_cur == NULL;
        num1_null = num1_cur == NULL;
      }
      
    }

    Digit *get_last_digit() {
      return last_digit;
    }
};

BigNum* subtract( BigNum *bignum0, BigNum *bignum1 ) {
  // cases:
  // both positive: subtract bigger - smaller
  // bignum0 positive, bignum1 negative: add bignum0 + bignum1 as positives, get rid of negative sign
  // bignum0 negative, bignum1 positive: add bignum0 + bignum1 as positives, make result negative
  // bignum0 negative, bignum1 negative:
  //  if( bignum1 > bignum0 ): subtract bignum1 - bignum0 as positives, result is positive
  //  else: subtract bignum0 - bignum1 as positives, result is negative
  
};

// num0 should be at least as long as bignum1, and should be
// greater in value
// change this so we don't modify in place, create a new bignum
BigNum* _subtract( BigNum *bignum0, BigNum *bignum1 ) {
  std::cout << "Subtract" << std::endl;
  Digit *num0_cur = bignum0 -> get_last_digit();
  Digit *num1_cur = bignum1 -> get_last_digit();

  BigNum *difference_bignum = new BigNum();

  short num0_cur_val, num1_cur_val;
  Digit *previous_digit;

  bool num0_null = num0_cur == NULL;
  bool num1_null = num1_cur == NULL;

  while( !num0_null ) {
    num0_cur_val = num0_cur -> value;
    num1_cur_val = (num1_null) ? 0 : num1_cur -> value;

    // need to find a value that we can borrow from
    if( num0_cur_val < num1_cur_val ) {
      previous_digit = num0_cur -> prev_digit;
      while( previous_digit -> value == 0 ) {
        // update this digit to be 9
        previous_digit -> value = 9;
        previous_digit = previous_digit -> prev_digit;
      }
      // subtract 1 from that digit to borrow
      previous_digit -> value -= 1;
      num0_cur_val += 10;
    }
    num0_cur -> value = num0_cur_val - num1_cur_val;

    num0_cur = (num0_null) ? NULL : num0_cur -> prev_digit;
    num1_cur = (num1_null) ? NULL : num1_cur -> prev_digit;

    num0_null = num0_cur == NULL;
    num1_null = num1_cur == NULL;
  }

};

int main(int argc, char **argv) {
  int i;

  short bignum_0[] = {5, 2, 1};
  short bignum_1[] = {4, 5, 6};

  BigNum *bignum0 = new BigNum(bignum_0, 3);
  BigNum *bignum1 = new BigNum(bignum_1, 3);

  bignum0 -> display();
  bignum1 -> display();

  // // add the two
  // bignum0.add(bignum1);
  // subtract the two
  BigNum *result = subtract(bignum0, bignum1);

  result -> display();

  bignum0 -> delete_bignum();
  bignum1 -> delete_bignum();
  result -> delete_bignum();

  delete bignum0;
  delete bignum1;
  delete result;

  return 0;
}