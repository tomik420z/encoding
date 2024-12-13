def ConvertToStr(bytesData):
    return ''.join([chr(s) for s in bytesData])

def IsPng(data):
    keySequence = [137, 80]
    return keySequence == data[:2]

def IsBmp(data):
    if len(data) < 2:
        return False
    keySequence = [66, 77]
    return keySequence == data[:2]

def FindSubsequence(sequence, subsequence):
    return [(i, i + len(subsequence)) for i in range(len(sequence)) if sequence[i:i + len(subsequence)] == subsequence]