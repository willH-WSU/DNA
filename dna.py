DEBUG = False

class dna:
    """
    This class implements the DNA alphabet.
    """

    PADDING_CHAR = 'A'
    SYMBOLS_PER_WORD = 4
    WORD_SIZE = 8  # bits

    # String representation of bits
    alphabet = {'A': '00', 'C': '01', 'G': '10', 'T': '11'}
    encoding = {'00': 'A', '01': 'C', '10': 'G', '11': 'T'}

    def interleave(sequence1, sequence2):
        """
        Combine the ith character (from 0 to n)  of two sequences to create a new sequence.  
        """
        newSequence = ''
        i = 0
        while i < len(sequence1):
            newSequence += sequence1[i] + sequence2[i]
            i += 1
        return newSequence

    def needsPadding(sequence):
        """
        Returns 'True' if the length of a given 'sequence' is not a multiple of the SYBMOLS_PER_WORD.
        """
        if len(sequence) % dna.SYMBOLS_PER_WORD != 0:
            if DEBUG:
                print('Needs padding!')
            return True
        else:
            if DEBUG:
                print('Does not need padding.')
            return False

    def pack(sequence):
        sequence = dna.pad(sequence)
        packedSequence = ''
        i = 0
        while i < len(sequence):
            binarySequence = '0b'	# Binary prefix
            block = sequence[i:i+dna.SYMBOLS_PER_WORD]
            if DEBUG:
                print(block)
            for char in block:
                if DEBUG:
                    print(char)
                binarySequence += dna.alphabet[char.upper()]
            if DEBUG:
                print(binarySequence)
            # Convert string representation of binary word(s) to int, then char.
            packedSequence += chr(eval(binarySequence))
            i += dna.SYMBOLS_PER_WORD
        return packedSequence

    def pad(sequence):
        """
        Returns the given 'sequence' padded with 'A' to lengthen the 'sequence' to a multiple of SYMBOLS_PER_WORD.
        """
        if dna.needsPadding(sequence):
            paddedSequence = sequence
            charsToPad = dna.SYMBOLS_PER_WORD - len(sequence) % dna.SYMBOLS_PER_WORD
            if DEBUG:
                print('Chars to padd = ', charsToPad)
            for char in range (0, charsToPad):
                paddedSequence += dna.PADDING_CHAR
            return paddedSequence
        else:
            return sequence

    def padLength(sequence, length):
        """
        Returns the given 'sequence' padded with 'A' to lengthen the 'sequence' to a given 'length' and a 
        multiple of SYMBOLS_PER_WORD.
        """
        paddedSequence = sequence
        while len(paddedSequence) < length:
            paddedSequence += dna.PADDING_CHAR
        paddedSequence = dna.pad(paddedSequence)  # Ensure multiple of dna.WORD_SIZE
        return paddedSequence

    def unpack(sequence):
        """
        Returns DNA 'symbols' given a packed 'sequence'.
        """

        symbols = ''
        for char in sequence:
            bString = bin(ord(char))
            bString = bString[2::]  # Remove binary prefix '0b'
            # Left pad with zeros to ensure |bString| = dna.WORD_SIZE
            bString = bString.zfill(dna.WORD_SIZE)
            b1 = bString[0:2]
            b2 = bString[2:4]
            b3 = bString[4:6]
            b4 = bString[6:8]
            symbolBlock = dna.encoding[b1] + dna.encoding[b2] + dna.encoding[b3] + dna.encoding[b4]
            symbols += symbolBlock
        return symbols


if __name__ == '__main__':
    """
    Self tests
    """

    # 1. Check padding w/ 4 symbol sequence
    a1 = 'CCCC'
    result = dna.needsPadding(a1)
    if(not result):
        print('1. Check padding w/ 4 symbol sequence: \t\tpass')
    else:
        print('1. Check padding w/ 4 symbol sequence: \t\tFAIL')

    # 2. Check padding w/ < 4 symbol sequence
    a1 = 'CC'
    result = dna.needsPadding(a1)
    if(result):
        print('2. Check padding w/ < 4 symbol sequence: \tpass')
    else:
        print('2. Check padding w/ < 4 symbol sequence: \tFAIL')

    # 3. Pad sequence of < 4 symbol sequence
    a1 = 'CC'
    result = dna.pad(a1)
    if result == 'CCAA':
        print('3. Pad string of < 4 symbols: \t\t\tpass')
    else:
        print('3. Pad string of < 4 symbols: \t\t\tFAIL ', result)

    # 4. Pad sequence of 4 symbols
    a1 = 'CCCC'
    result = dna.pad(a1)
    if result == 'CCCC':
        print('4. Pad string of 4 symbols: \t\t\tpass')
    else:
        print('4. Pad string of 4 symbols: \t\t\tFAIL ', result)

    # 5. Pad sequence of > 4 symbols
    a1 = 'CCCCG'
    result = dna.pad(a1)
    if result == 'CCCCGAAA':
        print('5. Pad string of > 4 symbols: \t\t\tpass')
    else:
        print('5. Pad string of > 4 symbols: \t\t\tFAIL ', result)

    # 6. Pack sequence of < 4 symbols
    a1 = 'CC'
    result = dna.pack(a1)
    if result == 'P':
        print('6. Pack string of < 4 symbols: \t\t\tpass')
    else:
        print('6. Pack string of < 4 symbols: \t\t\tFAIL')

    # 7. Pack sequence of 4 symbols
    a1 = 'CCCC'
    result = dna.pack(a1)
    if result == 'U':
        print('7. Pack string of 4 symbols: \t\t\tpass')
    else:
        print('7. Pack string of 4 symbols: \t\t\tFAIL', result)

    # 8. Pack sequence of > 4 symbols
    # a1 = 'CCCCG'
    a1 = 'AGACCAGA'
    result = dna.pack(a1)
    # if result == 'P\x80':
    if result == '!H':
        print('8. Pack string of >4 symbols: \t\t\tpass')
    else:
        print('8. Pack string of >4 symbols: \t\t\tFAIL', result)
        

    # 9. Unpack sequence of one character
    s1 = 'w'
    result = dna.unpack(s1)
    if result == 'CTCT':
        print('9. Unpack string of 1 symbol: \t\t\tpass')
    else:
        print('9. Unpack string of 1 symbol: \t\t\tFAIL', result)

    # 10. Unpack sequence of two characters
    s1 = 'w '
    result = dna.unpack(s1)
    if result == 'CTCTAGAA':
        print('10. Unpack string of 2 symbols: \t\tpass')
    else:
        print('10. Unpack string of 2 symbols: \t\tFAIL', result)

    # 11. Pad sequence of 4 symbols to 6, resulting in 8 symbols.
    s1 = 'CCGG'
    result = dna.padLength(s1, 6)
    if result == 'CCGGAAAA':
        print('11. Pad string of 4 symbols to 6 -> 8: \t\tpass')
    else:
        print('11. Pad string of 4 symbols to 6 -> 8: \t\tFAIL', result)

    # 12. Interleave two sequences.
    s1 = 'AAAA'
    s2 = 'TTTT'
    result = dna.interleave(s1, s2)
    if result == 'ATATATAT':
        print('12. Interleave two strings: \t\t\tpass')
    else:
        print('12. Interleave two strings: \t\t\tFAIL', result)

    # X. Dump alphabet as integers
    print('X. Dump \Sigma:')
    print('   A = ', dna.alphabet['A'])
    print('   C = ', dna.alphabet['C'])
    print('   G = ', dna.alphabet['G'])
    print('   T = ', dna.alphabet['T'])
