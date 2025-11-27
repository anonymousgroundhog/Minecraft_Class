from mcpi.minecraft import Minecraft
import mcpi.block as block
import time

# Connect to Minecraft
mc = Minecraft.create()
pos = mc.player.getTilePos()

mc.postToChat("Hello Minecraft World")
mc.postToChat("Constructing IT 359/360 Castle & Syllabus...")

# --- Configuration ---
base_x = pos.x + 5
base_y = pos.y
base_z = pos.z + 5

size = 85 # Slightly larger to fit all signs comfortably
wall_height = 10
tower_height = 14
material = block.COBBLESTONE.id

# ==========================================
# CASTLE CONSTRUCTION FUNCTIONS
# ==========================================

def build_wall_segment(x1, z1, x2, z2, orientation):
    # 1. Solid Wall
    mc.setBlocks(x1, base_y, z1, x2, base_y + wall_height, z2, material)
    # 2. Machicolations & Battlements
    if orientation == 'NS': 
        mc.setBlocks(x1 - 1, base_y + wall_height, z1, x1 - 1, base_y + wall_height, z2, material)
        for z in range(z1, z2 + 1, 2):
            mc.setBlock(x1 - 1, base_y + wall_height + 1, z, material) 
            mc.setBlock(x2, base_y + wall_height + 1, z, material)      
    else: 
        mc.setBlocks(x1, base_y + wall_height, z1 - 1, x2, base_y + wall_height, z1 - 1, material)
        for x in range(x1, x2 + 1, 2):
            mc.setBlock(x, base_y + wall_height + 1, z1 - 1, material) 
            mc.setBlock(x, base_y + wall_height + 1, z2, material)      

def build_tower(x, z):
    mc.setBlocks(x, base_y, z, x + 4, base_y + tower_height, z + 4, material)
    mc.setBlocks(x - 1, base_y + tower_height, z - 1, x + 5, base_y + tower_height, z + 5, material)
    for i in range(0, 7, 2):
        mc.setBlock(x - 1 + i, base_y + tower_height + 1, z - 1, material)
        mc.setBlock(x - 1 + i, base_y + tower_height + 1, z + 5, material)
        mc.setBlock(x - 1, base_y + tower_height + 1, z - 1 + i, material)
        mc.setBlock(x + 5, base_y + tower_height + 1, z - 1 + i, material)

# --- Build Structure ---
mc.postToChat("Building Walls...")
# Towers
build_tower(base_x, base_z)
build_tower(base_x + size, base_z)
build_tower(base_x, base_z + size)
build_tower(base_x + size, base_z + size)

# Walls
build_wall_segment(base_x + 4, base_z + 4, base_x + 4, base_z + size, 'NS') # West
build_wall_segment(base_x + size, base_z + 4, base_x + size, base_z + size, 'NS') # East
build_wall_segment(base_x + 4, base_z + size, base_x + size, base_z + size, 'EW') # South

# Split North Wall (Gate)
center_x = base_x + 4 + ((size - 4) // 2)
build_wall_segment(base_x + 4, base_z + 4, center_x - 2, base_z + 4, 'EW')
build_wall_segment(center_x + 2, base_z + 4, base_x + size, base_z + 4, 'EW')

# Gatehouse
gate_z = base_z + 4
mc.setBlocks(center_x - 3, base_y, gate_z - 2, center_x - 1, base_y + wall_height, gate_z, material)
mc.setBlocks(center_x + 1, base_y, gate_z - 2, center_x + 3, base_y + wall_height, gate_z, material)
mc.setBlocks(center_x - 3, base_y + 5, gate_z - 2, center_x + 3, base_y + wall_height, gate_z, material)
# Clear Air
mc.setBlocks(center_x - 1, base_y, gate_z - 3, center_x + 1, base_y + 4, gate_z + 1, block.AIR.id)
# Welcome Sign
mc.setSign(center_x + 2, base_y, gate_z - 3, 63, 8, "Welcome", "to", "IT 359/360", "Syllabus")

# Water/Moat
mc.postToChat("Filling Moat...")
moat_width = 4
moat_level = base_y - 1
WATER = 9
mc.setBlocks(base_x - 1 - moat_width, moat_level, base_z - 1 - moat_width, base_x + size + 5 + moat_width, moat_level, base_z - 1 - 1, WATER) # N
mc.setBlocks(base_x - 1 - moat_width, moat_level, base_z + size + 5 + 1, base_x + size + 5 + moat_width, moat_level, base_z + size + 5 + moat_width, WATER) # S
mc.setBlocks(base_x - 1 - moat_width, moat_level, base_z - 1, base_x - 1 - 1, moat_level, base_z + size + 5, WATER) # W
mc.setBlocks(base_x + size + 5 + 1, moat_level, base_z - 1, base_x + size + 5 + moat_width, moat_level, base_z + size + 5, WATER) # E
mc.setBlocks(center_x - 1, base_y, base_z - 1 - moat_width, center_x + 1, base_y, base_z - 1 - 1, 5) # Bridge

# ==========================================
# COMPREHENSIVE SYLLABUS SIGNS
# ==========================================
mc.postToChat("Placing Syllabus Signs...")

syllabus_data = [
    # --- PAGE 1 ---
    ["=== PAGE 1 ===", "IT 359", "Pen Testing", "Updated 9/15/25"],
    ["Note:", "Support Hours", "M/W/F", "9 AM - 5 PM"],
    ["Instructor:", "Dr. Sean Sanders", "spsand1@ilstu", "Room: JH 028"],
    ["Class Time:", "12:35-1:50 PM", "Mon / Wed", ""],
    ["Student Support:", "Hours:", "By appointment", ""],
    
    # --- PAGE 2 ---
    ["=== PAGE 2 ===", "Overview:", "Pen Testing &", "Ethical Hacking"],
    ["Outcomes 1:", "Malicious vs", "Ethical Hacking", "Frameworks"],
    ["Outcomes 2:", "Data Gathering", "Footprinting", "Enumeration"],
    ["Outcomes 3:", "Intrusions", "Escalate Privs", "Trojans/Exfil"],
    ["Outcomes 4:", "Threat Hunting", "Proactive/Anomaly", "Threat Models"],
    ["Outcomes 5:", "Incident Resp", "Live Analysis", "Malware Analys", "Post-Mortem"],
    ["Knowledge 1:", "Cyber Fundmntls", "Ethics & Diffs", "Offensive Skill"],
    ["Knowledge 2:", "Threat Intel", "Actor Profiles", "IOCs"],
    ["Knowledge 3:", "Incident Resp", "Static/Dynamic", "Analysis"],

    # --- PAGE 3 ---
    ["=== PAGE 3 ===", "Technology:", "School IT Reqs", "Reliable Net"],
    ["Comm:", "Class Website", "Check Email", "Regularly"],
    ["Contact:", "Email Prof", "Allow time", "for response"],
    ["Textbook/Lab:", "HackTheBox", "VIP+ Sub", "$20 per month"],

    # --- PAGE 4 ---
    ["=== PAGE 4 ===", "Optional Mats:", "IEEE Security", "ACM Transact"],
    ["Journals:", "Computers & Sec", "Info Sec Jrnl", "Reggienet"],
    ["Format:", "60% Lecture", "40% Lab", "Concepts->Lab"],

    # --- PAGE 5 ---
    ["=== PAGE 5 ===", "Grading:", "Labs: 40%", "Partic: 10%"],
    ["Grading Cont:", "Project: 20%", "Exams: 30%", "(2 @ 15%)"],
    ["Scoring:", "Out of 100", "Weighted", "No indiv grades"],

    # --- PAGE 6 ---
    ["=== PAGE 6 ===", "Scale:", "A: 90.00+", "B: 80-89.99"],
    ["Scale Cont:", "C: 70-79.99", "D: 60-69.99", "F: < 59.99"],
    ["PASSING REQ:", "MUST SCORE >60", "IN ALL PARTS", "TO PASS!"],
    ["Failure Ex:", "Lab=40, Rest=90", "result is F", "Must pass all"],
    ["Curving:", "Components:", "NO Curve", "Cutoffs: Maybe"],

    # --- PAGE 7 ---
    ["=== PAGE 7 ===", "Quizzes:", "Weekly/Canvas", "Start of class"],
    ["Quiz Info:", "10-20 Mins", "Read AHEAD", "of class"],
    ["Exams:", "Includes", "Challenges", ""],
    ["Labs:", "Hands-on Tools", "Submit Canvas", "Strict Deadline"],
    ["Lab Policy:", "Late Work", "NOT Graded", "Canvas Only"],

    # --- PAGE 8 ---
    ["=== PAGE 8 ===", "Attendance:", "Expected", "Hard to catchup"],
    ["Excused Abs:", "Quarantine", "Death in Fam", "Mil/Jury Duty"],
    ["Not Excused:", "Weddings", "Vacations", "Sports"],
    ["If Excused:", "Notify BEFORE", "Email Prof AND", "Form to Dean"],
    ["Unexcused 1:", "1-2 Misses:", "No Makeups", "No Pts"],
    ["Unexcused 2:", "3 Misses:", "Grade Drop", "Letter Down"],
    ["Unexcused 3:", "4+ Misses:", "Course F", "Fail"],
    ["Lateness:", "Come anyway", "Enter quietly", "No makeup actv"],

    # --- PAGE 9 ---
    ["=== PAGE 9 ===", "Preparation:", "Read Material", "Before Class"],
    ["Accommodat:", "Student Access", "350 Fell Hall", "309-438-5853"],
    ["Basic Needs:", "Food/Housing", "Contact Dean", "of Students"],
    ["Mental Health:", "SCS Services", "320 Stu Svcs", "309-438-3655"],
    ["MH Support:", "Free/Confid", "Kognito Sim", "Help friends"],

    # --- PAGE 10 (Schedule) ---
    ["=== PAGE 10 ===", "Schedule:", "Wk 1-2: Intro", "Ethical Hack"],
    ["Wk 1-2:", "Footprinting", "Nmap", "Attack Surface"],
    ["Wk 3:", "Exploits", "Bin Path Hijack", "Sudo Perms"],
    ["Wk 3 Cont:", "Vuln Scan", "Brute Force", "HTB Tier 2"],
    ["Wk 4-8:", "Red Team Intro", "Frameworks", "OSINT"],
    ["Wk 4-8 Cont:", "Recon", "Methodologies", "Team Proj Idea"],
    ["Week 9:", "Midterm Review", "MIDTERM EXAM", "March 8"],
    ["Wk 10-16:", "Spring Break", "Attack Frmwrk", "MITRE ATT&CK"],
    ["Week 17:", "Student Pres", "FINAL EXAM", ""]
]

# --- Sign Placement Logic ---
# Path: West Wall (S) -> South Wall (E) -> East Wall (N)
# We place signs on the block directly inside the wall.

# Initial Coords
current_x = base_x + 5
current_z = base_z + 5
wall_stage = 1 # 1=West(moving S), 2=South(moving E), 3=East(moving N)

sign_spacing = 2 # Every other block

for sign_lines in syllabus_data:
    # Ensure lines list has 4 elements
    lines = sign_lines + [""] * (4 - len(sign_lines))
    
    # Place Sign
    if wall_stage == 1: # West Wall, facing East (Text faces player looking West)
        # Orientation 4 is West, 12 is East. 
        # If sign is on West wall, player looks West to read it? 
        # Actually, sign on West wall faces East (towards center). ID 12.
        mc.setSign(current_x, base_y, current_z, 63, 12, lines[0], lines[1], lines[2], lines[3])
        current_z += sign_spacing
        
        # Check corner
        if current_z >= base_z + size - 5:
            wall_stage = 2
            current_x += sign_spacing
            current_z = base_z + size - 5 # Lock Z

    elif wall_stage == 2: # South Wall, facing North
        # Sign on South wall faces North. ID 0 (South) or 8 (North). 
        # Usually 0 faces player looking South? No, 0 faces South.
        # We want sign to face North (into courtyard). ID 8? 
        # Let's use 0. If backwards, use 8. (Standard is 0=South, 8=North).
        # We want the text facing North. So sign backs to South wall.
        mc.setSign(current_x, base_y, current_z, 63, 0, lines[0], lines[1], lines[2], lines[3])
        current_x += sign_spacing
        
        # Check corner
        if current_x >= base_x + size - 5:
            wall_stage = 3
            current_z -= sign_spacing
            current_x = base_x + size - 5 # Lock X

    elif wall_stage == 3: # East Wall, facing West
        # Sign on East wall faces West. ID 4.
        mc.setSign(current_x, base_y, current_z, 63, 4, lines[0], lines[1], lines[2], lines[3])
        current_z -= sign_spacing

# Teleport player to start
mc.player.setPos(base_x + 10, base_y, base_z + 10)
mc.postToChat("Syllabus Complete!")
