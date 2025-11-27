from mcpi.minecraft import Minecraft
from mcpi import block
import time

# --- CONFIGURATION ---
# Connect to the game (default localhost:4711)
mc = Minecraft.create()

# Get player position to build near them
px, py, pz = mc.player.getTilePos()

# Building Materials
WALL_MAT = block.STONE_BRICK.id
FLOOR_MAT = block.WOOL.id
FLOOR_COLOR = 14  # Red wool for a carpet look
ROOF_MAT = block.GLASS.id
LIGHT_MAT = block.GLOWSTONE_BLOCK.id

# Syllabus Data (Formatted for Signs)
syllabus_walls = [
    {
        "name": "General Info",
        "signs": [
            ["IT 359", "Pen Testing", "Tools & Tech", "Fall 2025"], # [cite: 1]
            ["Dr. Sanders", "JH 028", "spsand1@", "ilstu.edu"],    # [cite: 4]
            ["Mon & Wed", "12:35 PM", "to", "1:50 PM"],            # [cite: 4]
            ["Support Hrs:", "M/W/F", "9AM - 5PM", "By Appt"]      # [cite: 4]
        ]
    },
    {
        "name": "The Rules",
        "signs": [
            ["ATTENDANCE", "1-2: 0 pts", "3: Grade drop", "4: FAIL"], # [cite: 120-122]
            ["! WARNING !", "Must pass", "ALL PARTS", "with >60"],    # [cite: 85]
            ["Example:", "If Lab=40", "But Exam=90", "GRADE = F"],    # [cite: 86]
        ]
    },
    {
        "name": "Grading & Loot",
        "signs": [
            ["Labs: 40%", "Exams: 30%", "Project: 20%", "Partic: 10%"], # [cite: 74]
            ["Scale:", "A: 90+", "B: 80-89", "C: 70-79"],               # [cite: 78-81]
            ["Scale Cont:", "D: 60-69", "F: < 60", ""],                 # [cite: 82-83]
            ["REQUIRED:", "HackTheBox", "VIP+ Sub", "$20/Month"]        # [cite: 59]
        ]
    },
    {
        "name": "Timeline",
        "signs": [
            ["Wk 1-2:", "Intro/Ethical", "Footprinting", "Nmap / Ports"], # [cite: 142]
            ["Wk 3:", "Binary Path", "Sudo Perms", "Brute Force"],        # [cite: 142]
            ["Wk 4-8:", "Red Team", "OSINT/Recon", "Frameworks"],         # [cite: 142]
            ["WEEK 9", "Review &", "MIDTERM EXAM", "Mar 8"],              # [cite: 142]
            ["Wk 10-16", "Attack Frmwrk", "MITRE", "ATT&CK/ATLAS"],       # [cite: 142]
            ["WEEK 17", "Presentations", "FINAL EXAM", "Good Luck!"]      # [cite: 142]
        ]
    },
    {
        "name": "Skill Tree",
        "signs": [
            ["Diff: Malicious", "vs Ethical", "Frameworks &", "Consequences"], # [cite: 12, 13]
            ["Recon:", "Data Gather", "& Footprint", "Enumeration"],           # [cite: 14, 15]
            ["Attack:", "Intrusions", "Priv Escalate", "Trojans"],             # [cite: 16-18]
            ["Hunting:", "Threat Hunt", "Anomaly Detect", "Threat Models"],    # [cite: 19-22]
            ["Response:", "Live Analysis", "Malware (S/D)", "Post-Mortem"]     # [cite: 24-26]
        ]
    },
    {
        "name": "Quest Board",
        "signs": [
            ["Labs on", "HackTheBox", "Digital", "Forensics"],      # [cite: 59, 100]
            ["SUBMIT VIA", "CANVAS ONLY", "No Email", "Subs"],      # [cite: 101]
            ["Deadline:", "Submit BEFORE", "Late Work", "= NO GRADE"], # [cite: 102]
            ["FAIL COND:", "If Lab Avg", "is < 60%", "FAIL COURSE"] # [cite: 85]
        ]
    },
    {
        "name": "Safety/Support",
        "signs": [
            ["Accomms?", "Stud. Access", "350 Fell Hall", "309-438-5853"],   # [cite: 131]
            ["Website:", "StudentAccess.", "IllinoisState", ".edu"],         # [cite: 131]
            ["Basic Needs", "Food/Housing", "Contact Dean", "of Students"],  # [cite: 134]
            ["Mental Health", "Stressed?", "Call SCS", "309-438-3655"]       # [cite: 137]
        ]
    }
]

# --- BUILD LOGIC ---

# 1. Calculate Building Size
total_signs = sum(len(section["signs"]) for section in syllabus_walls)
# Add spacing for section headers
total_length = total_signs * 2 + (len(syllabus_walls) * 4) + 5 

# Building Start Coordinate (shifted away from player so they don't spawn inside)
bx = px + 3
by = py
bz = pz

print(f"Building Syllabus Hall... Length: {total_length}")

# 2. Clear Area (Air)
mc.setBlocks(bx, by, bz, bx + total_length, by + 5, bz + 6, block.AIR.id)

# 3. Construct Shell (Floor, Ceiling, Walls)
# Floor (Red Wool)
mc.setBlocks(bx, by - 1, bz, bx + total_length, by - 1, bz + 6, FLOOR_MAT, FLOOR_COLOR)
# Ceiling (Glass)
mc.setBlocks(bx, by + 4, bz, bx + total_length, by + 4, bz + 6, ROOF_MAT)
# Back Wall (Stone Brick) - This is where signs go
mc.setBlocks(bx, by, bz + 5, bx + total_length, by + 3, bz + 5, WALL_MAT)
# Front Wall (Glass Panes or low wall) - Let's do a low fence for visibility
mc.setBlocks(bx, by, bz - 1, bx + total_length, by, bz - 1, block.FENCE.id)

# 4. Create Entrance
# Remove fence at start
mc.setBlocks(bx, by, bz - 1, bx + 2, by, bz - 1, block.AIR.id)
# Create a Stone Arch
mc.setBlocks(bx, by, bz, bx, by + 4, bz + 5, block.STONE.id)
mc.setBlock(bx, by+1, bz+2, block.TORCH.id, 5) # Torch on arch

# 5. Place Signs and Lighting
current_x = bx + 2 # Start 2 blocks in

for section in syllabus_walls:
    # Place a header sign (Standing sign on floor)
    # 63 is Standing Sign. Block 8 is floor rotation.
    mc.setBlock(current_x, by, bz + 2, 63, 8) 
    mc.setSign(current_x, by, bz + 2, 63, 8, 
               "== SECTION ==", 
               section["name"], 
               "=============", 
               "")
    
    current_x += 2 # Move forward
    
    for sign_text in section["signs"]:
        # Ensure we don't crash if text is missing
        l1 = sign_text[0] if len(sign_text) > 0 else ""
        l2 = sign_text[1] if len(sign_text) > 1 else ""
        l3 = sign_text[2] if len(sign_text) > 2 else ""
        l4 = sign_text[3] if len(sign_text) > 3 else ""
        
        # Place Wall Sign
        # ID 68 is Wall Sign. Data 2 faces North (towards Z-). 
        # Since our wall is at Z+5 facing Z-, we use data value 2.
        mc.setBlock(current_x, by + 2, bz + 4, 68, 2)
        mc.setSign(current_x, by + 2, bz + 4, 68, 2, l1, l2, l3, l4)
        
        # Add a Glowstone in the floor every other sign for lighting
        if current_x % 2 == 0:
            mc.setBlock(current_x, by - 1, bz + 2, LIGHT_MAT)
            
        current_x += 2 # Leave a 1 block gap between signs
        
    current_x += 3 # Gap between sections

# 6. Teleport Player to Entrance
mc.player.setPos(bx - 2, by, bz + 2)
print("Build Complete! Welcome to the Syllabus Hall.")
