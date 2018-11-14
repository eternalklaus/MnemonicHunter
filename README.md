# MnemonicHacker
- Developed by Jiwon Choi 
- jiwon.choi@kaist.ac.kr
<br>  

## About MnemonicHacker
MnemonicHacker list up instructions that using designated mnemonic operand.  
This application leverages https://c9x.me.  
<br>  

## Install

    git clone https://github.com/eternalklaus/MnemonicHacker.git
    cd MnemonicHacker
    python MnemonicHacker.py
<br>  

## Example
Lets search about instruction for effective address computation.  
Mnemonic `r/m` and `m32` means memory reference, so let's search about it.   

    python MnemonicHacker.py "r/m" "m32"

As the same manner, search instructions using *immediate 4byte value* as operand.

    python MnemonicHacker.py "imm32"
<br>  

## Mnemonic
You can use those mnemonics for searching. 

| Mnemonic | Information | Description |
|:--------|:--------|:--------|
| /digit | OPCODE | ModR/M byte of the instruction uses only the r/m (register or memory) operand. Digit is 0~7 |
| /r | OPCODE | ModR/M byte of the instruction contains both a register operand and an r/m operand. |
| cb,cw,cd,cp | OPCODE | 1-byte (cb), 2-byte (cw), 4-byte (cd) or 6-byte (cp) value |
| r32 | INSTRUCTION | 32-bit doubleword register |
| imm32 | INSTRUCTION | 32-bit immediate doubleword value |
| r/m32 | INSTRUCTION | 32-bit doubleword register or memory operand. |
| m32 | INSTRUCTION | a memory doubleword addressed by DS:SI or ES:DI (used only by string instructions).  |

<br>  

Need more information about assembler mnemonic? see [here](http://www.uobabylon.edu.iq/uobColeges/ad_downloads/6_2708_780.pdf).
