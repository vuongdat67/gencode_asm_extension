# ================= TESTCASE 1: Basic Assignments & Conversions =================
# convert to hexadecimal a random integer between 1 and 100 and append it to the string a
# append string '0x' to a
# increment a by 1
# cast a to int16
# ba1 is a bytearrary of ba1
# compute absolute value of subfs, add it to the first 2 chars of rev_suplx (base 32), then convert to hex
# check if y is not x

# Output:
# a += '\\x%02x' % random . randint ( 1 , 100 )
# a += var0
# a += 1
# a = int ( hopcode , 16 )
# var1 = bytearray ( var1 )
# digits_d = hex ( abs ( abs ( base ) ) + var2 [ 0 : 2 ] , 16 )
# if y is not xor

# ================= TESTCASE 2: String & Hex Manipulation =================
# initialize bad_chars to the string '\x0a\x00\x0d'
# remove '\\x' from the second argument, decode it in hexadecimal, and save in bad_chars
# add the bytes literal "\x02\x00\x01\xbb" to the variable buf
# Convert the variable x to a hexadecimal and store it in the variable y
# append the value x converted in hex to the string y
# Convert the variable x to a hexadecimal and add it to the variable z followed by ','
# print the string '[-] ' concatenated with the variable error_msg
# Output:
# bad_chars = '\x0a\x0\x0\x0\x0
# var2 = hex ( sys . pop ( '\\x' ) , decode ( '\\x' ) )
# var2 += b'\x02\xbb\x01\xbb\x03\x01\xbb\xbf'
# y = '%02x' % x
# y += '%02x' % x
# z += '%02x, ' % x
# print ( '[-]' + var1 )


# ================= TESTCASE 3: Bitwise Operations =================
# assign the variable y the bytearray of shellcode at index 0 bitwise xor bytearray of shellcode at index 1
# assign the variable y to x bitwise xor the bytearray of shellcode at index n
# compute bitwise xor of y and the first element of shellcode converted into a byte array
# set the variable y to x bitwise xor of 0x88
# compute bitwise xor of the first element in shellcode and the second element of shellcode
# y is not x (bitwise NOT operation)
# Output:
# y = var0 ( var1 ) [ 0 ] ^ bytearray ( var0 ) [ 1 ]
# y = x ^ var0 ( ) [ n ]
# if y ^ xor
# y = x ^ var0
# return var0 [ 0 ] ^ var1 [ 1 ]
# y = ~ x

# ================= TESTCASE 4: Data Structures & Functions =================
# bad_app_labels is an empty set
# call the import_string with argument backend, substitute it for backend_cls
# builtins is a dictionary with 3 initial entries: True, False, and None
# double the chunk_size
# define the function 'first' with an argument 'value'
# get the first element of the list shellcode
# Output:
# bad_label = set ( )
# var2 = var0 ( var2 )
# builtins = { 'true' : True , var0 , var1 ]
# d = var1 * 2
# def var0 ( 'first' ) :
# var1 = var0 [ 0 ]

# ================= TESTCASE 5: Control Flow =================
# break loop execution
# break from the loop execution
# breaks from the smallest enclosing loop
# exit from the iteration
# break the cycle
# skip this loop iteration
# continue the loop
# Output:
# break
# break
# break
# break
# break
# continue
# continue

# Logs:
# PS C:\Users\vuong\Documents\upload\dev1> & C:/Users/vuong/Documents/upload/dev1/.venv/Scripts/Activate.ps1
# (.venv) PS C:\Users\vuong\Documents\upload\dev1> python pyd_http.py
# Serving ExploitGen Python HTTP on http://127.0.0.1:9138/infer
# [REQ] len=19 source='check if y is not x' sim='check if y is not x'
# Some weights of RobertaModel were not initialized from the model checkpoint at fg-codebert and are newly initialized: ['pooler.dense.bias', 'pooler.dense.weight']
# You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
# Some weights of RobertaModel were not initialized from the model checkpoint at fg-codebert and are newly initialized: ['pooler.dense.bias', 'pooler.dense.weight']
# You should probably TRAIN this model on a down-stream task to be able to use it for predictions and inference.
# 从...model/python/checkpoint-best-rouge/pytorch_model.bin...重新加载参数
# C:\Users\vuong\Documents\upload\dev1\model.py:148: UserWarning: The torch.cuda.*DtypeTensor constructors are no longer recommended. It's best to use methods such as torch.tensor(data, dtype=*, device='cuda') to create tensors. (Triggered internally at C:\actions-runner\_work\pytorch\pytorch\pytorch\torch\csrc\tensor\python_tensor.cpp:80.)
#   zero = torch.cuda.LongTensor(1).fill_(0)
# [REQ] len=87 source='convert to hexadecimal a random integer between 1 and 100 and append it to the string a' sim='convert to hexadecimal a random integer between 1 and 100 and append it to the string a'
# [REQ] len=23 source='append string '0x' to a' sim='append string '0x' to a'
# [REQ] len=16 source='increment a by 1' sim='increment a by 1'
# [REQ] len=15 source='cast a to int16' sim='cast a to int16'
# [REQ] len=26 source='ba1 is a bytearrary of ba1' sim='ba1 is a bytearrary of ba1'
# [REQ] len=104 source='compute absolute value of subfs, add it to the first 2 chars of rev_suplx (base 32), then convert to hex' sim='compute absolute value of subfs, add it to the first 2 chars of rev_suplx (base 32), then convert to hex'
# [REQ] len=19 source='check if y is not x' sim='check if y is not x'
# [REQ] len=49 source='initialize bad_chars to the string '\x0a\x00\x0d'' sim='initialize bad_chars to the string '\x0a\x00\x0d''
# [REQ] len=86 source='remove '\\x' from the second argument, decode it in hexadecimal, and save in bad_chars' sim='remove '\\x' from the second argument, decode it in hexadecimal, and save in bad_chars'
# [REQ] len=60 source='add the bytes literal "\x02\x00\x01\xbb" to the variable buf' sim='add the bytes literal "\x02\x00\x01\xbb" to the variable buf'
# [REQ] len=70 source='Convert the variable x to a hexadecimal and store it in the variable y' sim='Convert the variable x to a hexadecimal and store it in the variable y'
# [REQ] len=51 source='append the value x converted in hex to the string y' sim='append the value x converted in hex to the string y'
# [REQ] len=84 source='Convert the variable x to a hexadecimal and add it to the variable z followed by ','' sim='Convert the variable x to a hexadecimal and add it to the variable z followed by ',''
# [REQ] len=64 source='print the string '[-] ' concatenated with the variable error_msg' sim='print the string '[-] ' concatenated with the variable error_msg'
# [REQ] len=105 source='assign the variable y the bytearray of shellcode at index 0 bitwise xor bytearray of shellcode at index 1' sim='assign the variable y the bytearray of shellcode at index 0 bitwise xor bytearray of shellcode at index 1'
# [REQ] len=76 source='assign the variable y to x bitwise xor the bytearray of shellcode at index n' sim='assign the variable y to x bitwise xor the bytearray of shellcode at index n'
# [REQ] len=87 source='compute bitwise xor of y and the first element of shellcode converted into a byte array' sim='compute bitwise xor of y and the first element of shellcode converted into a byte array'
# [REQ] len=43 source='set the variable y to x bitwise xor of 0x88' sim='set the variable y to x bitwise xor of 0x88'
# [REQ] len=89 source='compute bitwise xor of the first element in shellcode and the second element of shellcode' sim='compute bitwise xor of the first element in shellcode and the second element of shellcode'
# [REQ] len=34 source='y is not x (bitwise NOT operation)' sim='y is not x (bitwise NOT operation)'
# [REQ] len=30 source='bad_app_labels is an empty set' sim='bad_app_labels is an empty set'
# [REQ] len=75 source='call the import_string with argument backend, substitute it for backend_cls' sim='call the import_string with argument backend, substitute it for backend_cls'
# [REQ] len=70 source='builtins is a dictionary with 3 initial entries: True, False, and None' sim='builtins is a dictionary with 3 initial entries: True, False, and None'
# [REQ] len=21 source='double the chunk_size' sim='double the chunk_size'
# [REQ] len=52 source='define the function 'first' with an argument 'value'' sim='define the function 'first' with an argument 'value''
# [REQ] len=43 source='get the first element of the list shellcode' sim='get the first element of the list shellcode'
# [REQ] len=20 source='break loop execution' sim='break loop execution'
# [REQ] len=29 source='break from the loop execution' sim='break from the loop execution'
# [REQ] len=39 source='breaks from the smallest enclosing loop' sim='breaks from the smallest enclosing loop'
# [REQ] len=23 source='exit from the iteration' sim='exit from the iteration'
# [REQ] len=15 source='break the cycle' sim='break the cycle'
# [REQ] len=24 source='skip this loop iteration' sim='skip this loop iteration'
# [REQ] len=17 source='continue the loop' sim='continue the loop'