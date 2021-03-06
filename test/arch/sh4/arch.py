import time
from pdb import pm
from sys import stderr
from miasm2.arch.sh4.arch import *
from miasm2.core.asmblock import AsmSymbolPool

symbol_pool = AsmSymbolPool()

def h2i(s):
    return s.replace(' ', '').decode('hex')

reg_tests_sh4 = [
    # vxworks
    ("c80022f2    MOV        0x10, R6",
     "10e6"),
    ("c8002250    MOV        0xFFFFFFFF, R0",
     "ffe0"),
    ("c800226a    MOV.W      @(PC,0xC0), R9",
     "5e99"),
    ("c8002006    MOV.L      @(PC & 0xFFFFFFFC,0x10), R15",
     "03df"),
    ("c800cfc4    MOV        R4, R9",
     "4369"),
    ("C8005004    MOV.B      R1, @R2",
     "1022"),
    ("C8002E04    MOV.W      R0, @R8",
     '0128'),
    ("c800223e    MOV.L      R1, @R14",
     "122E"),

    ("c8002002    MOV.L      @R1, R0",
     "1260"),
    ("c8002E08    MOV.W      @R8, R1",
     "8161"),
    ("c800357c    MOV.B      @R4, R1",
     "4061"),

    ("c8002220    MOV.L      R8, @-R15",
     "862f"),
    ("c8022a66    MOV.B      R4, @-R0",
     "4420"),
    ("c8002310    MOV.L      @R15+, R14",
     "f66e"),
    ("c80038a4    MOV.W      @R8+, R5",
     "8565"),
    ("xxxxxxxx    MOV.B      R0, @(R8,0x2)",
     "8280"),
    ("xxxxxxxx    MOV.W      R0, @(R8,0x4)",
     "8281"),
    ("c8002274    MOV.L      R0, @(R9,0x8)",
     "0219"),
    ("xxxxxxxx    MOV.B      @(R8,0x8), R0",
     "8884"),
    ("xxxxxxxx    MOV.W      @(R8,0x10), R0",
     "8885"),
    ("c8002500    MOV.L      @(R14,0x4), R5",
     "e155"),
    ("xxxxxxxx    MOV.B      R4, @(R0,R8)",
     "4408"),
    ("xxxxxxxx    MOV.W      R4, @(R0,R8)",
     "4508"),
    ("xxxxxxxx    MOV.L      R4, @(R0,R8)",
     "4608"),
    ("xxxxxxxx    MOV.B      @(R0,R4), R8",
     "4c08"),
    ("xxxxxxxx    MOV.W      @(R0,R4), R8",
     "4d08"),
    ("xxxxxxxx    MOV.L      @(R0,R4), R8",
     "4e08"),
    ("xxxxxxxx    MOV.B      R0, @(GBR,0x4)",
     "04c0"),
    ("xxxxxxxx    MOV.W      R0, @(GBR,0x8)",
     "04c1"),
    ("xxxxxxxx    MOV.L      R0, @(GBR,0x10)",
     "04c2"),
    ("xxxxxxxx    MOV.B      @(GBR,0x4), R0",
     "04c4"),
    ("xxxxxxxx    MOV.W      @(GBR,0x8), R0",
     "04c5"),
    ("xxxxxxxx    MOV.L      @(GBR,0x10), R0",
     "04c6"),
    #("xxxxxxxx    MOV        PC & 0xFFFFFFFC+0x14, R0",
    # "04c7"),
    ("xxxxxxxx    SWAPB      R2, R1",
     "2861"),
    ("c803f492    SWAPW      R4, R9",
     "4969"),
    ("xxxxxxxx    XTRCT      R4, R9",
     "4d29"),
    ("c8002270    ADD        R12, R9",
     "cc39"),
    ("c8002238    ADD        0xFFFFFFFC, R15",
     "FC7F"),
    ("c80164cc    ADDC       R0, R1",
     "0e31"),
    ("xxxxxxxx    ADDV       R0, R1",
     "0f31"),
    ("c8002994    CMPEQ      0x20, R0",
     "2088"),
    ("c80029d2    CMPEQ      R2, R1",
     "2031"),
    ("c8003964    CMPHS      R5, R3",
     "5233"),
    ("c8002df2    CMPGE      R0, R1",
     "0331"),
    ("c80029a4    CMPHI      R1, R0",
     "1630"),
    ("c8002bfe    CMPGT      R10, R8",
     "a738"),
    ("c8002bf8    CMPPZ      R0",
     "1140"),
    ("c8006294    CMPPL      R2",
     "1542"),
    ("c8033800    CMPSTR     R14, R4",
     "ec24"),
    ("xxxxxxxx    DIV1       R14, R4",
     "e434"),
    ("c8d960de    DIV0S      R0, R3",
     "0723"),
    ("xxxxxxxx    DIV0U      ",
     "1900"),
    ("c800dcd8    DMULS      R1, R0",
     "1d30"),
    ("c80164da    DMULU      R3, R8",
     "3538"),
    ("c80024e2    DT         R10",
     "104a"),
    ("c800343a    EXTSB      R1, R1",
     "1e61"),
    ("c8002bf6    EXTSW      R0, R0",
     "0f60"),
    ("c8002fba    EXTUB      R0, R0",
     "0c60"),
    ("c8002398    EXTUW      R0, R0",
     "0d60"),
    ("xxxxxxxx    MAC.L      @R5+, @R4+",
     "5f04"),
    ("xxxxxxxx    MAC.W      @R5+, @R4+",
     "5f44"),
    ("c8005112    MULL       R1, R3",
     "1703"),
    ("xxxxxxxx    MULSW      R1, R3",
     "1F23"),
    ("xxxxxxxx    MULUW      R1, R3",
     "1e23"),
    ("c8004856    NEG        R1, R8",
     "1b68"),
    ("c80054fc    NEGC       R9, R7",
     "9a67"),
    ("c8004b36    SUB        R1, R5",
     "1835"),
    ("c800a536    SUBC       R1, R0",
     "1a30"),
    ("xxxxxxxx    SUBV       R1, R0",
     "1b30"),
    ("c80023ca    AND        R0, R5",
     "0925"),
    ("c800257c    AND        0x2, R0",
     "02c9"),
    ("xxxxxxxx    AND.B      0x2, @(GBR,R0)",
     "02cd"),
    ("c80065fe    NOT        R5, R1",
     "5761"),
    ("c8002586    OR         R10, R1",
     "ab21"),
    ("c80023aa    OR         0x4, R0",
     "04cb"),
    ("xxxxxxxx    OR.B       0x4, @(GBR,R0)",
     "04cf"),
    ("xxxxxxxx    TAS.B      @R8",
     "1b48"),
    ("c8002368    TST        R10, R13",
     "a82d"),
    ("c8003430    TST        0x11, R0",
     "11c8"),
    ("xxxxxxxx    TST.B      0x4, @(GBR,R0)",
     "04cc"),
    ("c8003978    XOR        R1, R6",
     "1a26"),
    ("c8028270    XOR        0x1, R0",
     "01ca"),
    ("xxxxxxxx    XOR.B      0x4, @(GBR,R0)",
     "04cE"),
    ("xxxxxxxx    ROTL       R9",
     "0449"),
    ("xxxxxxxx    ROTR       R9",
     "0549"),
    ("xxxxxxxx    ROTCL      R9",
     "2449"),
    ("xxxxxxxx    ROTCR      R9",
     "2549"),
    ("xxxxxxxx    SHAL       R11",
     "204b"),
    ("xxxxxxxx    SHAR       R11",
     "214b"),
    ("c800236c    SHLD       R6, R10",
     "6d4a"),
    ("xxxxxxxx    SHLL       R11",
     "004b"),
    ("xxxxxxxx    SHLR       R11",
     "014b"),
    ("xxxxxxxx    SHLL2      R11",
     "084b"),
    ("xxxxxxxx    SHLR2      R11",
     "094b"),
    ("xxxxxxxx    SHLL8      R11",
     "184b"),
    ("xxxxxxxx    SHLR8      R11",
     "194b"),
    ("xxxxxxxx    SHLL16     R11",
     "284b"),
    ("xxxxxxxx    SHLR16     R11",
     "294b"),
    ("c8002c00    BF         0xFFFFFFF4",
     "f48b"),
    ("c80023c2    BFS        0xFFFFFFD8",
     "d88f"),
    ("c8002266    BT         0x5B",
     "5b89"),
    ("c8002266    BTS        0x5C",
     "5c8d"),
    ("c8002326    BRA        0xFFFFFFF0",
     "f0af"),
    ("c8004b4a    BRAF       R1",
     "2301"),
    ("c8055da4    BSR        0xFFFFFE48",
     "48be"),
    ("xxxxxxxx    BSRF       R1",
     "0301"),
    ("c80027b4    JMP.L      @R1",
     "2b41"),
    ("c800200c    JSR.L      @R0",
     "0b40"),
    ("c800231a    RTS        ",
     "0b00"),
    ("xxxxxxxx    CLRMAC     ",
     "2800"),
    ("xxxxxxxx    CLRS       ",
     "4800"),
    ("xxxxxxxx    CLRT       ",
     "0800"),
    ("c8002004    LDC        R0, SR",
     "0e40"),
    ("c800200e    LDC        R1, GBR",
     "1e41"),
    ("c8064bd4    LDC        R8, VBR",
     "2e48"),
    ("xxxxxxxx    LDC        R8, SSR",
     "3e48"),
    ("xxxxxxxx    LDC        R8, SPC",
     "4e48"),
    ("xxxxxxxx    LDC        R8, DBR",
     "fa48"),
    ("xxxxxxxx    LDC        R8, R0_BANK",
     "8e48"),
    ("xxxxxxxx    LDC.L      @R8+, SR",
     "0748"),
    ("xxxxxxxx    LDC.L      @R8+, GBR",
     "1748"),
    ("xxxxxxxx    LDC.L      @R8+, VBR",
     "2748"),
    ("xxxxxxxx    LDC.L      @R8+, SSR",
     "3748"),
    ("xxxxxxxx    LDC.L      @R8+, SPC",
     "4748"),
    ("xxxxxxxx    LDC.L      @R8+, DBR",
     "f648"),
    ("xxxxxxxx    LDC.L      @R8+, R2_BANK",
     "a748"),
    ("xxxxxxxx    LDS        R8, MACH",
     "0a48"),
    ("xxxxxxxx    LDS        R8, MACL",
     "1a48"),
    ("xxxxxxxx    LDS        R8, PR",
     "2a48"),
    ("xxxxxxxx    LDS.L      @R8+, MACH",
     "0648"),
    ("xxxxxxxx    LDS.L      @R8+, MACL",
     "1648"),
    ("xxxxxxxx    LDTLB      ",
     "3800"),
    ("xxxxxxxx    MOVCA.L    R0, @R8",
     "c308"),
    ("xxxxxxxx    NOP        ",
     "0900"),
    ("xxxxxxxx    OCBI.L     @R8",
     "9308"),
    ("xxxxxxxx    OCBP.L     @R8",
     "a308"),
    ("xxxxxxxx    OCBWB.L    @R8",
     "b308"),
    ("xxxxxxxx    PREF.L     @R8",
     "8308"),
    ("xxxxxxxx    STS        MACH, R8",
     "0a08"),
    ("xxxxxxxx    STS        MACL, R8",
     "1a08"),
    ("xxxxxxxx    STS        PR, R8",
     "2a08"),
    ("xxxxxxxx    STS.L      MACH, @-R8",
     "0248"),
    ("xxxxxxxx    STS.L      MACL, @-R8",
     "1248"),
    ("xxxxxxxx    STS.L      PR, @-R8",
     "2248"),





    ("c8004b50    STC        GBR, R0",
     "1200"),
    ("c8064516    STC        VBR, R1",
     "2201"),
    ("c8004b54    STC        SSR, R1",
     "3201"),
    ("c801ed6c    STC        SPC, R0",
     "4200"),
    ("xxxxxxxx    STC        SGR, R0",
     "3a00"),
    ("xxxxxxxx    STC        DBR, R0",
     "fa00"),
    ("c8004b56    STC        R3_BANK, R1",
     "B201"),
    ("xxxxxxxx    STC.L      SR, @-R8",
     "0348"),
    ("xxxxxxxx    STC.L      GBR, @-R8",
     "1348"),
    ("xxxxxxxx    STC.L      VBR, @-R8",
     "2348"),
    ("xxxxxxxx    STC.L      SSR, @-R8",
     "3348"),
    ("xxxxxxxx    STC.L      SPC, @-R8",
     "4348"),
    ("xxxxxxxx    STC.L      DBR, @-R8",
     "f248"),
    ("xxxxxxxx    STC.L      R7_BANK, @-R8",
     "f348"),
    ("c803b130    TRAPA      0xE0",
     "e0c3"),

    ("xxxxxxxx    FLDI0      FR8",
     "8df8"),
    ("xxxxxxxx    FLDI1      FR8",
     "9df8"),
    ("c8019ca8    FMOV       FR15, FR5",
     "fcf5"),
    ("c800affe    FMOV.S     @R1, FR4",
     "18f4"),
    ("c80283f6    FMOV.S     @(R0,R14), FR5",
     "e6f5"),
    ("c800aff8    FMOV.S     @R1+, FR5",
     "19f5"),
    ("c80cb692    FMOV.S     FR0, @R2",
     "0af2"),
    ("c80cb694    FMOV.S     FR1, @-R2",
     "1bf2"),
    ("c80283aa    FMOV.S     FR1, @(R0,R14)",
     "17fe"),
    ("c800ce16    FLDS       FR13, FPUL",
     "1dfd"),
    ("c800ce08    FSTS       FPUL, FR13",
     "0dfd"),
    ("xxxxxxxx    FABS       FR8",
     "5df8"),
    ("c800cf28    FADD       FR2, FR6",
     "20f6"),
    ("c805dacc    FCMPEQ     FR2, FR6",
     "24f6"),
    ("c8028406    FCMPGT     FR4, FR2",
     "45f2"),
    ("c8019ca4    FDIV       FR2, FR12",
     "23fc"),
    ("c800ce5e    FLOAT      FPUL, FR2",
     "2df2"),
    ("xxxxxxxx    FMAC       FR0, FR1, FR2",
     "1ef2"),
    ("c800b006    FMUL       FR2, FR4",
     "22f4"),
    ("c805e412    FNEG       FR14",
     "4dfe"),
    ("xxxxxxxx    FSQRT      FR14",
     "6dfe"),
    ("c8030400    FSUB       FR4, FR2",
     "41f2"),
    ("c80303ba    FTRC       FR2, FPUL",
     "3df2"),

]

for s, l in reg_tests_sh4:
    print "-" * 80
    s = s[12:]
    b = h2i((l))
    print b.encode('hex')
    mn = mn_sh4.dis(b, None)
    print [str(x) for x in mn.args]
    print s
    print mn
    assert(str(mn) == s)
    l = mn_sh4.fromstring(s, symbol_pool, None)
    assert(str(l) == s)
    a = mn_sh4.asm(l)
    print [x for x in a]
    print repr(b)
    assert(b in a)


# speed test
o = ""
for s, l, in reg_tests_sh4:
    s = s[12:]
    b = h2i((l))
    o += b

while len(o) < 1000:
    o += o
bs = bin_stream_str(o)
off = 0
instr_num = 0
ts = time.time()
while off < bs.getlen():
    mn = mn_sh4.dis(bs, None, off)
    print instr_num, off, mn.l, str(mn)
    instr_num += 1
    off += mn.l
print 'instr per sec:', instr_num / (time.time() - ts)

import cProfile
cProfile.run(r'mn_sh4.dis("\x17\xfe", None)')
