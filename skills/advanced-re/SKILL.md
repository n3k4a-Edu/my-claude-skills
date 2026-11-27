---
name: advanced-re
description: "Advanced reverse engineering, binary analysis, malware analysis, and software research. Use when the user asks about disassembling binaries, decompiling executables, analyzing malware, cracking CTF challenges, firmware analysis, protocol reverse engineering, anti-debug bypassing, packing/unpacking, or deep binary research. Supplements the reverse-engineer-anything skill with advanced techniques. For authorized security research, CTF, and educational purposes."
metadata:
  version: "1.0.0"
  author: "custom"
---

# Advanced Reverse Engineering

For authorized security research, CTF competitions, malware analysis, and educational binary research. Uses REA MCP, IDA MCP, and standard RE tools.

## Analysis Methodology

### Phase 1: Triage
1. File type identification: `file`, magic bytes, PE/ELF/Mach-O headers
2. Strings extraction: interesting URLs, error messages, registry keys, API endpoints
3. Import/export analysis: What APIs does it use? Networking? Crypto? File I/O?
4. Entropy analysis: High entropy sections = packed/encrypted
5. Digital signatures: Signed? By whom? Valid?

### Phase 2: Static Analysis
1. Disassemble with IDA/REA → identify main(), WinMain(), or entry point
2. Map the program flow: main loop, initialization, key functions
3. Identify interesting functions by:
   - String references ("License", "Activation", "Error", API URLs)
   - API calls (CreateFile, RegOpenKey, socket, send, recv)
   - Crypto usage (AES, RSA, hash functions)
4. Document data structures and their relationships
5. Rename functions and variables as you understand them

### Phase 3: Dynamic Analysis
1. Set breakpoints on key functions
2. Trace execution with specific inputs
3. Watch memory regions for modifications
4. Monitor API calls (Procmon, API Monitor, strace/ltrace)
5. Network capture if applicable (Wireshark)

## Common Protection Schemes

### Packing/Obfuscation
| Packer | Detection | Approach |
|---|---|---|
| UPX | "UPX!" header, 3 sections | `upx -d` or manual OEP finding |
| Themida/WinLicense | VM-based, high entropy | Trace to OEP, dump, fix IAT |
| VMProtect | Bytecode VM, handler chains | Identify VM handlers, trace bytecode |
| .NET Obfuscation | Confusing names, flow obfuscation | de4dot, then dnSpy |
| JavaScript obfuscation | eval chains, string encoding | AST-based deobfuscation, dynamic eval |

### Anti-Debug Techniques
| Technique | Detection | Bypass |
|---|---|---|
| IsDebuggerPresent | Checks PEB.BeingDebugged | Patch PEB or hook API |
| NtQueryInformationProcess | ProcessDebugPort | Return 0 |
| Timing checks (RDTSC) | Measures execution time | NOP or fix timing |
| Hardware breakpoint detection | GetThreadContext | Clear DR registers |
| Self-modifying code | Writes over own code | Trace carefully, snapshot |
| TLS callbacks | Runs before main | Set BP on TLS directory entry |

### License/Activation Systems
Common patterns:
1. **Serial check**: String comparison or hash verification → find the compare
2. **Online activation**: API call with hardware ID → find the success path
3. **Time trial**: Date comparison → find the check routine
4. **Feature flags**: Boolean checks → find and flip
5. **Certificate/signature**: RSA verification → find the verify call

## Protocol Reverse Engineering

1. Capture traffic (Wireshark, mitmproxy for HTTPS)
2. Identify packet structure: header, length, type, payload
3. Replay and modify packets
4. Map message types and their responses
5. Document the protocol specification

## Firmware Analysis

1. Extract firmware: binwalk, dd, firmware-mod-kit
2. Identify filesystem: squashfs, cramfs, JFFS2, UBIFS
3. Mount and explore the filesystem
4. Find: web interfaces, config files, SSH keys, hardcoded credentials
5. Identify the bootloader, kernel, main application
6. Cross-compile tools for the target architecture if needed

## CTF-Specific Techniques

### Binary Exploitation (Pwn)
- Buffer overflow: find the overflow, control EIP/RIP, ROP chain or shellcode
- Format string: %n write, GOT overwrite
- Heap exploitation: Use-after-free, double-free, heap overflow
- Return-oriented programming: gadget finding, chain building

### Reversing Challenges
- Identify the flag check algorithm
- Work backwards from the success condition
- Z3/angr for constraint solving on complex checks
- Side-channel analysis for timing-based challenges

## Automation with Python

```python
# Pattern: Automated binary analysis script
from pathlib import Path
import struct

def analyze_binary(filepath):
    data = Path(filepath).read_bytes()
    
    # Check PE header
    if data[:2] == b'MZ':
        pe_offset = struct.unpack_from('<I', data, 0x3C)[0]
        if data[pe_offset:pe_offset+4] == b'PE\x00\x00':
            print("PE executable")
            # Parse further...
    
    # Check ELF
    elif data[:4] == b'\x7fELF':
        print("ELF executable")
        # Parse further...
    
    # Entropy analysis
    from collections import Counter
    entropy = calculate_entropy(data)
    if entropy > 7.5:
        print("HIGH ENTROPY - likely packed/encrypted")

def calculate_entropy(data):
    import math
    counts = Counter(data)
    length = len(data)
    return -sum((c/length) * math.log2(c/length) for c in counts.values())
```

## Tool Integration

| Tool | Use for | In this environment |
|---|---|---|
| IDA Pro | Professional disassembly | IDA MCP (mcp__ida-multi-mcp__*) |
| REA | Automated RE workflows | REA MCP (mcp__rea__*) |
| Cheat Engine | Runtime memory analysis | CheatEngine MCP |
| Ghidra | Free disassembler/decompiler | If installed on system |
| x64dbg / WinDbg | Windows debugging | Via command line |
| GDB | Linux debugging | Via command line |
| Frida | Dynamic instrumentation | Via REA MCP or standalone |
| angr | Symbolic execution | Python library |
| Binary Ninja | Interactive disassembly | If installed |

## Ethics

- Authorized security research and testing: ✅
- CTF competitions: ✅
- Malware analysis (sandboxed): ✅
- Interoperability research: ✅
- Learning how software works: ✅
- Software piracy / crack distribution: ❌
- Bypassing protections on others' software for redistribution: ❌
