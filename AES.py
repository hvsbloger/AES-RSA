import socket



# S-Box
sBox = [
        0x9,
        0x4,
        0xA,
        0xB,
        0xD,
        0x1,
        0x8,
        0x5,
        0x6,
        0x2,
        0x0,
        0x3,
        0xC,
        0xE,
        0xF,
        0x7,
    ]

    # Inverse S-Box
sBoxI = [
        0xA,
        0x5,
        0x9,
        0xB,
        0x1,
        0x7,
        0x8,
        0xF,
        0x6,
        0x0,
        0x2,
        0x3,
        0xC,
        0x4,
        0xD,
        0xE,
    ]



    




    

def gf_mult(a, b):
    """Galois field multiplication of a and b in GF(2^4) / x^4 + x + 1
         a: First number
         b: Second number
        returns: Multiplication of both under GF(2^4)
        """
        # Initialise
    product = 0

        # Mask the unwanted bits
    a = a & 0x0F
    b = b & 0x0F

        # While both multiplicands are non-zero
    while a and b:

            # If LSB of b is 1
        if b & 1:

                # Add current a to product
            product = product ^ a

            # Update a to a * 2
        a = a << 1

            # If a overflows beyond 4th bit
            
        if a & (1 << 4):

                # XOR with irreducible polynomial with high term eliminated
            a = a ^ 0b10011

            # Update b to b // 2
        b = b >> 1

    return product

def int_to_state(n):
    """Convert a 2-byte integer into a 4-element vector (state matrix)
         m: integer
        :returns: state corresponding to the integer
        """
        
    return [n >> 12 & 0xF, (n >> 4) & 0xF, (n >> 8) & 0xF, n & 0xF]

    
def state_to_int(m):
    """Convert a 4-element vector (state matrix) into 2-byte integer
        : m: state
        :returns: integer corresponding to the state
        """
    return (m[0] << 12) + (m[2] << 8) + (m[1] << 4) + m[3]

def add_round_key(s1, s2):
        
    """Add round keys in GF(2^4)

         s1: First number
         s2: Second number
        :returns: Addition of both under GF(2^4)
        """
    return [i ^ j for i, j in zip(s1, s2)]

def sub_nibbles(sbox, state):
    """Nibble substitution

        sbox: Substitution box to use for transformatin
        state: State to perform sub nibbles transformation on
        :returns: Resultant state
        """
        
    return [sbox[nibble] for nibble in state]

def shift_rows(state):
    """Shift rows and inverse shift rows of state matrix (same)

        state: State to perform shift rows transformation on
        :returns: Resultant state
        """
        
    return [state[0], state[1], state[3], state[2]]

def mix_columns(state):
    """Mix columns transformation on state matrix

        state: State to perform mix columns transformation on
        :returns: Resultant state
        """
    return [
            state[0] ^ gf_mult(4, state[2]),
            state[1] ^ gf_mult(4, state[3]),
            state[2] ^ gf_mult(4, state[0]),
            state[3] ^ gf_mult(4, state[1]),
        ]

def inverse_mix_columns(state):
    """Inverse mix columns transformation on state matrix

        state: State to perform inverse mix columns transformation on
        :returns: Resultant state
        """
        
    return [
            gf_mult(9, state[0]) ^ gf_mult(2, state[2]),
            gf_mult(9, state[1]) ^ gf_mult(2, state[3]),
            gf_mult(9, state[2]) ^ gf_mult(2, state[0]),
            gf_mult(9, state[3]) ^ gf_mult(2, state[1]),
        ]

    
def encrypt(plaintext,key):
    """Encrypt plaintext with given key

        Example::

            ciphertext = SimplifiedAES(key=0b0100101011110101).encrypt(0b1101011100101000)

        plaintext: 16 bit plaintext
        :returns: 16 bit ciphertext
        """
    state = add_round_key(int_to_state(key),int_to_state(plaintext))
   
    
    state = sub_nibbles(sBox, state)
    
    
    state = shift_rows(state)
   
    
    state = mix_columns(state)
   

    #state = mix_columns(shift_rows(sub_nibbles(sBox, state)))

    state = add_round_key(int_to_state(key), state)
   
    
    state = sub_nibbles(sBox, state)
   
    
    state = shift_rows(state)
    

    #state = shift_rows(sub_nibbles(sBox, state))

    state =add_round_key(int_to_state(key), state)
   
    return state_to_int(state)

def decrypt(ciphertext,key):
    """Decrypt ciphertext with given key

        Example::

            plaintext = SimplifiedAES(key=0b0100101011110101).decrypt(0b0010010011101100)

        ciphertext: 16 bit ciphertext
        :returns: 16 bit plaintext
        """
    state = add_round_key(int_to_state(key), int_to_state(ciphertext))
   
    
    state = shift_rows(state)
    

    state = sub_nibbles(sBoxI, state)
   
    
    state = add_round_key(int_to_state(key), state)
   

    state = inverse_mix_columns(state)
   
    state = shift_rows(state)
    

    state = sub_nibbles(sBoxI, state)
    
    state = add_round_key(int_to_state(key), state)
    

    return state_to_int(state)


#key = 0b0100101011110101
