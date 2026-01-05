; =================TESTCASE 0: simple test=================
; add immediate to a byte variable
; increment esi
; load variable into ebx
; subtract 4 from esi
; push ebx to stack
; xor variable with 0xdb
; compare variable with 0xb
; jump if zero
; compute ebx + 0xf into eax
; load stack offset into esi
; shift ecx right by 2
; shift al right by 1
; compare ebx with another variable
; xor eax with ecx
; multiply eax by ebx
; move 4 into eax
; push esi
; push ebx

; Output:
; add byte[esi], exit
; inc esi
; mov ebx, 1
; sub esi, 4
; push ebx
; xor ebx, var0
; cmp ecx, var0
; jz 0x687
; cmp var0, 0xf0
; mov esi, esp
; shr ecx, 1
; shr al, 0x
; cmp var0, var
; xor var0, ecx
; mul ebx
; mov edx, 4
; push esi
; push ecx

; ================= TESTCASE 1: Basic Operations & Data Movement =================

; move the immediate value 100 into eax
; move the address of "var1" into edi
; load the value at the address stored in edi into ebx
; increment the value in ebx
; move the value of ebx into the memory location [esi + 4]
; swap the values of eax and ecx
; Output:
; mov eax, 100
; mov var2, var0
; lea ebx,[var0]
; inc esi
; mov [esi+4], ebx
; xchg var0, ecx


;  ================= TESTCASE 2: Arithmetic & Bitwise Logic =================
; multiply eax by the value 5 (use imul)
; divide the 64-bit value edx:eax by ebx
; bitwise AND eax with 0xFFFF
; bitwise OR ecx with edx
; shift ebx left by 4 bits
; rotate al right by 1 bit
; clear edx to zero using the XOR trick
; Output:
; mul 0x5
; div dword[eax]
; and var0, 0xf2
; or var0, ecx
; shshr var0, 4
; ror al, 0x
; xor var0, ecx

;  ================= TESTCASE 3: Control Flow & Comparison =================
; compare the value in eax with the constant 50
; jump to label "is_lower" if eax is less than 50
; compare ebx with ecx
; jump to label "is_equal" if they are equal
; decrement ecx and jump to label "start_loop" if ecx is not zero
; perform a bitwise test on bit 0 of eax (use test instruction)
; jump to label "bit_set" if the result is not zero
; Output:
; cmp ecx, 50
; jmp var0, 50
; cmp var0, ecx
; jz var0
; loopnz var2
; test var2, var0
; jnz _load_data

;  ================= TESTCASE 4: Stack & Effective Address (Complex) =================
; push the entire EFLAGS register onto the stack
; push eax, ebx, and ecx onto the stack in one sequence
; pop the top value of the stack into edi
; use LEA to calculate: eax = ebx + (ecx * 8) + 12
; load the stack pointer (esp) into ebp to set up a frame
; subtract 16 from the stack pointer to allocate local variables
; Output:
; push 0x80
; push 0x68732f2f \n push 0x6e69622f \n mov var0, esp
; pop esi
; shl var0, 12
; pop var0
; sub esp, 8

; ================= TESTCASE 5: Shellcode & Hex Formatting =================
; initialize bad_chars to the string '\x0a\x00\x0d'
; remove '\x' from the second command-line argument
; decode the argument in hexadecimal and save in bad_chars
; convert a random integer between 1 and 100 to hexadecimal
; append the hex value to the string a
; append the string '0x' to variable a
; add the bytes literal "\x02\x00\x01\xbb" to the variable buf
; convert the variable x to a hexadecimal and store it in y
; append the value x converted in hex to the string z followed by a comma
; Output:
; xor var0, 0x00
; pop ebx
; pop var0
; mov ecx, 100
; add eax, 64
; add eax, var0
; add byte[buff], 0x03
; mov dword[esi], 0x
; inc dword[esi], 0x

; ================= TESTCASE 6: Logic & Casting =================
; increment variable a by 1
; cast variable a to a 16-bit integer using base 16
; ba1 is a bytearray of variable ba1
; compute absolute value of subfs
; add it to the first 2 characters of rev_suplx interpreted as base 32
; convert the summation result to a hexadecimal string
; set the variable y to x bitwise xor with 0x88
; assign y the bytearray of shellcode at index 0 xor with bytearray of shellcode at index 1
; bitwise NOT the variable x and store in y
; Output:
; inc esi
; sub byte[esi], 16
; var0 var1, var0
; mov var0,[var0]
; add eax, 32
; sub esp, 0x
; xor ecx, ecx
; xor byte[esi], 0x7
; xor var0,[esi]

; ================= TESTCASE 7: Data Structures & Objects =================
; bad_app_labels is an empty set
; builtins is a dictionary with entries: True, False, and None
; call the import_string function with argument backend
; substitute the result for variable backend_cls
; check if y is not x
; double the chunk_size variable
; define a function named 'first' that takes an argument 'value'
; get the first element of the list shellcode
; Output:
; xor ecx, ecx
; and var0, 0x2
; test var0, var0
; sub cl, 0x
; mov eax, x
; mov var0, var0
; db var0, 1
; pop esi

; ================= TESTCASE 8: Control Flow & Iteration =================
; break from the current loop execution
; exit from the iteration
; skip this loop iteration and move to the next one
; break the smallest enclosing loop
; compare eax with 50 and jump if lower
; iterate through the shellcode byte array
; check if the bitwise test on bit 0 of eax is non-zero
; Output:
; inc esi
; jmp eax
; jinc esi
; not ecx
; cmp ecx, 50
; cmp byte[esi], 0x
; test var1, var0