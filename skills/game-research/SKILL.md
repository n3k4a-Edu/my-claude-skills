---
name: game-research
description: "Game reverse engineering, modding, memory analysis, and research. Use when the user asks about game hacking (single-player), Cheat Engine, memory editing, game modding, save file editing, game protocol analysis, Unity/Unreal modding, asset extraction, trainer creation, game internals research, or analyzing game binaries. For authorized security research and educational purposes."
metadata:
  version: "1.0.0"
  author: "custom"
---

# Game Research & Modding

For authorized game research, modding, and single-player analysis. Uses tools available in this environment: Cheat Engine MCP, REA (Reverse Engineering Assistant), IDA MCP.

## Memory Analysis (Cheat Engine)

### Finding Values

1. **Known value scan**: Health = 100 → search 100 → take damage → search new value → narrow down
2. **Unknown value scan**: Don't know the value → "Unknown initial value" → changed/unchanged/increased/decreased
3. **Pointer scan**: Found address changes on restart → pointer scan → find base pointer chain
4. **Data type guide**:
   - Health/ammo (integer): 4 bytes, 2 bytes for older games
   - Health (float): Float type (many modern games)
   - Coordinates: Float or Double (x, y, z usually adjacent in memory)
   - Text/names: String type, UTF-8 or UTF-16
   - Flags/states: Byte or 1 byte (0/1 for booleans)

### Pointer Chains

```
Base Address (static) → Offset1 → Offset2 → ... → Final Value
[game.exe+0x1A2B3C] → +0x10 → +0x48 → +0x8 → Health
```

Steps:
1. Find the value address
2. "What accesses this address" → find the instruction
3. Look at the register + offset pattern
4. Pointer scan from the found address
5. Filter: Module must be the game exe, max level 5-7

### Structure Dissection

Once you have a pointer to an entity:
1. Open "Dissect data/structures" on the address
2. Group structures: 4-byte aligned, look for patterns
3. Common game object layout:
   - +0x00: VTable pointer
   - +0x08-0x20: Transform/Position (floats: x, y, z)
   - Variable: Health, mana, stats (floats or ints)
   - Variable: Pointers to inventory, equipment, etc.

## Binary Analysis (REA / IDA)

### Game Binary Analysis Flow

1. **Survey**: `binary_overview` → understand architecture, protections, engine
2. **Strings**: Search for interesting strings (menu text, error messages, config keys)
3. **Imports**: Check imported functions (graphics API, networking, file I/O)
4. **Key functions**: Find by string references, API calls, or vtable analysis
5. **Decompile**: Focus on game logic functions, not engine boilerplate

### Engine-Specific Patterns

**Unity (IL2CPP)**:
- `global-metadata.dat` contains type info
- Il2CppDumper extracts class structures
- Look for `GameManager`, `PlayerController`, `InventorySystem` classes
- Methods: `Update()`, `TakeDamage()`, `AddItem()`

**Unity (Mono)**:
- DLLs in `Managed/` folder (Assembly-CSharp.dll)
- Decompile with dnSpy or ILSpy
- Modify and recompile directly

**Unreal Engine**:
- UObject system with reflection
- GNames/GObjects arrays for runtime enumeration
- Blueprint functions callable via UFunction
- SDK generation with UE4SS or similar

**Custom engines**:
- Find the main loop (while + sleep/vsync pattern)
- Locate entity list (array of pointers, usually near player pointer)
- Trace from rendering → entity → properties

## Modding Approaches

| Approach | Complexity | Persistence |
|---|---|---|
| Memory editing (CE) | Low | Per-session |
| Save file editing | Low | Permanent |
| DLL injection / hooks | Medium | Per-session |
| Asset replacement | Medium | Permanent |
| Source mod (if available) | High | Permanent |
| Binary patching | High | Permanent |

### Save File Analysis

1. Find save location (AppData, Documents, game folder)
2. Identify format: JSON, XML, SQLite, binary, protobuf
3. For binary saves:
   - Look for magic bytes / header
   - Search for known values (player name, gold amount)
   - Map the structure
   - Check for checksums (CRC32 at end, modify and recalculate)

### Asset Extraction

- Unity: AssetStudio, UABE (Unity Asset Bundle Extractor)
- Unreal: UModel / FModel
- Custom: Identify archive format, write extractor
- Common formats inside: DDS/BC7 textures, FBX/glTF meshes, FMOD/Wwise audio

## Trainer / Tool Development

For creating game research tools:

```python
# Basic memory reader/writer framework
import ctypes
from ctypes import wintypes

kernel32 = ctypes.windll.kernel32

PROCESS_ALL_ACCESS = 0x1F0FFF

def read_memory(handle, address, size):
    buffer = ctypes.create_string_buffer(size)
    kernel32.ReadProcessMemory(handle, address, buffer, size, None)
    return buffer.raw

def write_memory(handle, address, data):
    kernel32.WriteProcessMemory(handle, address, data, len(data), None)
```

## Ethics & Scope

- Single-player modding and research: ✅
- Educational reverse engineering: ✅
- Understanding game mechanics and internals: ✅
- Creating accessibility mods: ✅
- Online/multiplayer cheating: ❌ (violates ToS, harms other players)
- Circumventing DRM for piracy: ❌
- Distributing cracks: ❌
