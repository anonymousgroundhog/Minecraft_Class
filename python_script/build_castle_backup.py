#
from mcpi.minecraft import Minecraft
import mcpi.block as block
import time
import random
import math

# Connect to Minecraft
mc = Minecraft.create()
pos = mc.player.getTilePos()

mc.postToChat("Hello Minecraft World")
mc.postToChat("Constructing Castle, Syllabus & Improved Treehouse...")

# --- Configuration ---
base_x = pos.x + 20
base_y = pos.y
base_z = pos.z + 20

size = 85 
wall_height = 10
tower_height = 14
material = block.COBBLESTONE.id

# --- MATERIALS ---
SPRUCE_PLANKS = (5, 1)
DARK_OAK_PLANKS = (5, 5)
DARK_OAK_LOG = (17, 1) 
LEAVES = 18 
FENCE = 85
GLASS_PANE = 102
GLOWSTONE = 89 
STAIRS_WOOD = 53
TORCH = 50
AIR = 0
WALL_SIGN = 68

# ==========================================
# CASTLE CONSTRUCTION FUNCTIONS
# ==========================================

def build_wall_segment(x1, z1, x2, z2, orientation):
    mc.setBlocks(x1, base_y, z1, x2, base_y + wall_height, z2, material)
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
    torch_y = base_y + tower_height + 2
    mc.setBlock(x - 1, torch_y, z - 1, TORCH, 5)
    mc.setBlock(x + 5, torch_y, z - 1, TORCH, 5)
    mc.setBlock(x - 1, torch_y, z + 5, TORCH, 5)
    mc.setBlock(x + 5, torch_y, z + 5, TORCH, 5)

def build_courtyard_floor(x1, z1, x2, z2):
    SANDSTONE = 24
    STONE_BRICK = 98
    mc.setBlocks(x1, base_y - 1, z1, x2, base_y - 1, z2, SANDSTONE)
    for x in range(x1, x2 + 1):
        for z in range(z1, z2 + 1):
            if (x + z) % 2 == 1:
                mc.setBlock(x, base_y - 1, z, STONE_BRICK)

def build_central_keep(cx, cz):
    floor_height = 6     
    num_floors = 4
    tower_height = floor_height * num_floors
    WOOD_PLANKS = 5
    STAIRS_STONE = 67
    
    mc.setBlocks(cx - 5, base_y, cz - 5, cx + 5, base_y + tower_height, cz + 5, material)
    mc.setBlocks(cx - 4, base_y + 1, cz - 4, cx + 4, base_y + tower_height + 5, cz + 4, AIR)
    
    mc.setBlocks(cx - 3, base_y, cz + 5, cx + 3, base_y + 5, cz + 9, material) 
    mc.setBlocks(cx - 2, base_y + 1, cz + 5, cx + 2, base_y + 4, cz + 8, AIR)   
    mc.setBlocks(cx, base_y, cz + 9, cx, base_y + 2, cz + 9, AIR)                
    mc.setBlocks(cx, base_y, cz + 5, cx, base_y + 3, cz + 5, AIR)                
    mc.setBlock(cx, base_y + 3, cz + 10, TORCH, 3) 

    top_y = base_y + tower_height
    mc.setBlocks(cx - 6, top_y, cz - 6, cx + 6, top_y, cz + 6, material)
    mc.setBlocks(cx - 6, top_y + 1, cz - 6, cx + 6, top_y + 1, cz + 6, material)
    mc.setBlocks(cx - 5, top_y + 1, cz - 5, cx + 5, top_y + 5, cz + 5, AIR)
    for i in range(-6, 7, 2):
        mc.setBlock(cx + i, top_y + 2, cz - 6, material) 
        mc.setBlock(cx + i, top_y + 2, cz + 6, material) 
        mc.setBlock(cx - 6, top_y + 2, cz + i, material) 
        mc.setBlock(cx + 6, top_y + 2, cz + i, material) 
    mc.setBlock(cx - 5, top_y + 2, cz, TORCH, 1) 
    mc.setBlock(cx + 5, top_y + 2, cz, TORCH, 2) 
    mc.setBlock(cx, top_y + 2, cz - 5, TORCH, 3) 
    mc.setBlock(cx, top_y + 2, cz + 5, TORCH, 4) 

    for i in range(num_floors):
        level_y = base_y + (i * floor_height)
        if i > 0:
            mc.setBlocks(cx - 4, level_y, cz - 4, cx + 4, level_y, cz + 4, WOOD_PLANKS)
        mc.setBlock(cx - 4, level_y + 3, cz, TORCH, 1)
        mc.setBlock(cx + 4, level_y + 3, cz, TORCH, 2)
        mc.setBlock(cx, level_y + 3, cz - 4, TORCH, 3)
        mc.setBlock(cx, level_y + 3, cz + 4, TORCH, 4)

    stair_y = base_y + 1
    sx, sz = cx + 4, cz + 4
    leg = 0 
    while stair_y < top_y + 1:
        if leg == 0:   orient = 3 
        elif leg == 1: orient = 1 
        elif leg == 2: orient = 2 
        elif leg == 3: orient = 0 
        mc.setBlock(sx, stair_y, sz, STAIRS_STONE, orient)
        mc.setBlocks(sx, stair_y + 1, sz, sx, stair_y + 3, sz, AIR)
        if stair_y % 6 == 0:
            t_id = 5
            if leg == 0: t_id = 2 
            elif leg == 1: t_id = 3 
            elif leg == 2: t_id = 1 
            elif leg == 3: t_id = 4 
            mc.setBlock(sx, stair_y + 2, sz, TORCH, t_id)
        if leg == 0: 
            sz -= 1
            if sz <= cz - 4: leg = 1 
        elif leg == 1: 
            sx -= 1
            if sx <= cx - 4: leg = 2
        elif leg == 2: 
            sz += 1
            if sz >= cz + 4: leg = 3
        elif leg == 3: 
            sx += 1
            if sx >= cx + 4: leg = 0
        stair_y += 1

# ==========================================
# TREEHOUSE & FOREST FUNCTIONS
# ==========================================

def is_safe_zone(tx, tz):
    buffer = 10
    forbidden_x1 = base_x - buffer
    forbidden_z1 = base_z - buffer
    forbidden_x2 = base_x + size + buffer
    forbidden_z2 = base_z + size + buffer
    if (tx >= forbidden_x1 and tx <= forbidden_x2 and 
        tz >= forbidden_z1 and tz <= forbidden_z2):
        return False 
    return True 

def build_hanging_lantern(x, y, z):
    mc.setBlock(x, y, z, FENCE)
    mc.setBlock(x, y - 1, z, GLOWSTONE)

def build_small_tree(tx, tz):
    height = random.randint(4, 6)
    mc.setBlocks(tx, base_y, tz, tx, base_y + height, tz, 17) 
    for y_off in range(height - 2, height + 2):
        for x_off in range(-2, 3):
            for z_off in range(-2, 3):
                if abs(x_off) + abs(z_off) <= 3:
                     if mc.getBlock(tx+x_off, base_y+y_off, tz+z_off) == 0:
                        mc.setBlock(tx+x_off, base_y+y_off, tz+z_off, 18)

def build_mega_tree_and_house(tx, tz):
    tree_height = 30
    house_floor_y = base_y + 20 
    
    # 1. Massive Trunk
    mc.setBlocks(tx-1, base_y, tz-1, tx+1, base_y + tree_height, tz+1, *DARK_OAK_LOG)
    
    # 2. Branches
    canopy_center_y = base_y + tree_height - 2
    for y_off in range(-2, 3):
        for i in range(1, 10):
            mc.setBlock(tx + i, canopy_center_y + y_off, tz, *DARK_OAK_LOG)
            mc.setBlock(tx - i, canopy_center_y + y_off, tz, *DARK_OAK_LOG)
            mc.setBlock(tx, canopy_center_y + y_off, tz + i, *DARK_OAK_LOG)
            mc.setBlock(tx, canopy_center_y + y_off, tz - i, *DARK_OAK_LOG)

    # 3. Canopy 
    canopy_radius = 12
    for dx in range(-canopy_radius, canopy_radius + 1):
        for dy in range(-4, 5): 
            for dz in range(-canopy_radius, canopy_radius + 1):
                if (dx**2 + dz**2 + (dy*2)**2) < canopy_radius**2:
                    if mc.getBlock(tx+dx, canopy_center_y+dy, tz+dz) == 0:
                         mc.setBlock(tx+dx, canopy_center_y+dy, tz+dz, LEAVES)

    mc.postToChat("Building Large Treehouse Deck...")
    
    # 4. LARGE Deck (Radius 8) - Built BEFORE stairs
    # Use Solid Planks
    deck_radius = 8
    mc.setBlocks(tx - deck_radius, house_floor_y, tz - deck_radius, 
                 tx + deck_radius, house_floor_y, tz + deck_radius, *SPRUCE_PLANKS)
    
    # Fence Railing (Radius 8)
    for i in range(-deck_radius, deck_radius + 1):
        mc.setBlock(tx+i, house_floor_y+1, tz-deck_radius, FENCE)
        mc.setBlock(tx+i, house_floor_y+1, tz+deck_radius, FENCE)
        mc.setBlock(tx-deck_radius, house_floor_y+1, tz+i, FENCE)
        mc.setBlock(tx+deck_radius, house_floor_y+1, tz+i, FENCE)
        
    # 5. CONTINUOUS WOOD STAIRS (The Drill)
    # We drill UP through the deck we just built
    curr_y = base_y + 1
    angle = 0
    stair_radius = 6 # Fits nicely between trunk (1) and rail (8)
    
    prev_sx, prev_sz = -999, -999 # Track previous stair pos
    
    while curr_y <= house_floor_y:
        sx = tx + int(stair_radius * math.cos(angle))
        sz = tz + int(stair_radius * math.sin(angle))
        
        # Orient Stair
        deg = math.degrees(angle) % 360
        stair_id = 0
        if 315 <= deg or deg < 45:   stair_id = 2 
        elif 45 <= deg < 135:        stair_id = 1 
        elif 135 <= deg < 225:       stair_id = 3 
        elif 225 <= deg < 315:       stair_id = 0 
        
        # Place Stair
        mc.setBlock(sx, curr_y, sz, STAIRS_WOOD, stair_id)
        
        # *** THE DRILL ***
        # Clear 3 blocks of HEADROOM above the stair. 
        # This overwrites the deck blocks when we get high enough.
        mc.setBlocks(sx, curr_y+1, sz, sx, curr_y+3, sz, AIR)
        
        # If we are at the top, clear the fence blocking the landing
        if curr_y == house_floor_y:
            # Clear forward path
            mc.setBlocks(sx-1, curr_y+1, sz-1, sx+1, curr_y+1, sz+1, AIR)

        # Increment Logic:
        # Only move Y up if we have moved X/Z (prevents vertical stacks)
        if sx != prev_sx or sz != prev_sz:
            curr_y += 1
            prev_sx = sx
            prev_sz = sz
        
        angle += 0.15 # Small increment to ensure no gaps

    # 6. Cabins
    h1_x1, h1_z1 = tx - 5, tz - 2
    h1_x2, h1_z2 = tx + 2, tz + 5
    # Force Floor
    mc.setBlocks(h1_x1, house_floor_y, h1_z1, h1_x2, house_floor_y, h1_z2, *SPRUCE_PLANKS)
    # Walls
    mc.setBlocks(h1_x1, house_floor_y+1, h1_z1, h1_x2, house_floor_y+4, h1_z2, *SPRUCE_PLANKS)
    # Interior Air
    mc.setBlocks(h1_x1+1, house_floor_y+1, h1_z1+1, h1_x2-1, house_floor_y+4, h1_z2-1, AIR) 
    # Windows
    mc.setBlocks(h1_x1, house_floor_y+2, h1_z1+2, h1_x1, house_floor_y+3, h1_z1+3, GLASS_PANE) 
    # Doorway
    mc.setBlocks(h1_x1+1, house_floor_y+1, h1_z1, h1_x1+1, house_floor_y+2, h1_z1, AIR)
    # Roof
    for i in range(5):
        mc.setBlocks(h1_x1-1+i, house_floor_y+5+i, h1_z1, h1_x2+1-i, house_floor_y+5+i, h1_z2, *DARK_OAK_PLANKS)

    h2_x1, h2_z1 = tx + 1, tz - 5
    h2_x2, h2_z2 = tx + 5, tz - 1
    # Force Floor
    mc.setBlocks(h2_x1, house_floor_y, h2_z1, h2_x2, house_floor_y, h2_z2, *SPRUCE_PLANKS)
    # Walls
    mc.setBlocks(h2_x1, house_floor_y+1, h2_z1, h2_x2, house_floor_y+4, h2_z2, *SPRUCE_PLANKS)
    # Interior Air
    mc.setBlocks(h2_x1+1, house_floor_y+1, h2_z1+1, h2_x2-1, house_floor_y+4, h2_z2-1, AIR) 
    mc.setBlocks(h2_x1+1, house_floor_y+2, h2_z2, h2_x1+2, house_floor_y+3, h2_z2, GLASS_PANE) 
    # Doorway
    mc.setBlocks(h2_x1, house_floor_y+1, h2_z1+1, h2_x1, house_floor_y+2, h2_z1+1, AIR)
    # Roof
    for i in range(4):
        mc.setBlocks(h2_x1-1+i, house_floor_y+5+i, h2_z1, h2_x2+1-i, house_floor_y+5+i, h2_z2, *DARK_OAK_PLANKS)
        
    # Clear trunk passage
    mc.setBlocks(tx-1, house_floor_y+1, tz-1, tx+1, house_floor_y+4, tz+1, AIR)

    # Lanterns
    build_hanging_lantern(tx-8, house_floor_y+3, tz-8)
    build_hanging_lantern(tx+8, house_floor_y+3, tz+8)
    build_hanging_lantern(tx-8, house_floor_y+3, tz+8)
    build_hanging_lantern(tx+8, house_floor_y+3, tz-8)
    build_hanging_lantern(tx-4, house_floor_y+6, tz)
    build_hanging_lantern(tx+4, house_floor_y+6, tz)


# ==========================================
# EXECUTE BUILD
# ==========================================

# 1. CASTLE
mc.postToChat("Building Walls...")
build_tower(base_x, base_z)
build_tower(base_x + size, base_z)
build_tower(base_x, base_z + size)
build_tower(base_x + size, base_z + size)

build_wall_segment(base_x + 4, base_z + 4, base_x + 4, base_z + size, 'NS') 
build_wall_segment(base_x + size, base_z + 4, base_x + size, base_z + size, 'NS') 
build_wall_segment(base_x + 4, base_z + size, base_x + size, base_z + size, 'EW') 

center_x = base_x + 4 + ((size - 4) // 2)
build_wall_segment(base_x + 4, base_z + 4, center_x - 2, base_z + 4, 'EW')
build_wall_segment(center_x + 2, base_z + 4, base_x + size, base_z + 4, 'EW')

gate_z = base_z + 4
mc.setBlocks(center_x - 3, base_y, gate_z - 2, center_x - 1, base_y + wall_height, gate_z, material)
mc.setBlocks(center_x + 1, base_y, gate_z - 2, center_x + 3, base_y + wall_height, gate_z, material)
mc.setBlocks(center_x - 3, base_y + 5, gate_z - 2, center_x + 3, base_y + wall_height, gate_z, material)
mc.setBlocks(center_x - 1, base_y, gate_z - 3, center_x + 1, base_y + 4, gate_z + 1, block.AIR.id)

# Sign and Torch
mc.setBlock(center_x + 2, base_y + 2, gate_z - 3, WALL_SIGN, 2) 
mc.setSign(center_x + 2, base_y + 2, gate_z - 3, WALL_SIGN, 2, "Welcome", "to", "IT 359/360", "Syllabus") 
mc.setBlock(center_x + 2, base_y + 3, gate_z - 2, TORCH, 4) 

# 2. MOAT
mc.postToChat("Filling Moat...")
moat_width = 4
moat_level = base_y - 1
WATER = 9
mc.setBlocks(base_x - 1 - moat_width, moat_level, base_z - 1 - moat_width, base_x + size + 5 + moat_width, moat_level, base_z - 1 - 1, WATER) 
mc.setBlocks(base_x - 1 - moat_width, moat_level, base_z + size + 5 + 1, base_x + size + 5 + moat_width, moat_level, base_z + size + 5 + moat_width, WATER) 
mc.setBlocks(base_x - 1 - moat_width, moat_level, base_z - 1, base_x - 1 - 1, moat_level, base_z + size + 5, WATER) 
mc.setBlocks(base_x + size + 5 + 1, moat_level, base_z - 1, base_x + size + 5 + moat_width, moat_level, base_z + size + 5, WATER) 
mc.setBlocks(center_x - 1, base_y, base_z - 1 - moat_width, center_x + 1, base_y, base_z - 1 - 1, 5) 

# 3. INTERIOR
build_courtyard_floor(base_x + 5, base_z + 5, base_x + size - 1, base_z + size - 1)
keep_x = base_x + (size // 2)
keep_z = base_z + (size // 2)
build_central_keep(keep_x, keep_z)

# 4. SINGLE TREEHOUSE & SMALL FOREST
mc.postToChat("Growing One Treehouse & Small Forest...")
forest_radius = 80
center_world_x = base_x + size // 2
center_world_z = base_z + size // 2

# Build ONE Treehouse
treehouses_built = 0
attempts = 0
while treehouses_built < 1 and attempts < 100:
    rx = center_world_x + random.randint(-forest_radius, forest_radius)
    rz = center_world_z + random.randint(-forest_radius, forest_radius)
    if is_safe_zone(rx, rz):
        build_mega_tree_and_house(rx, rz)
        treehouses_built += 1
    attempts += 1

# Build Forest of SMALL Trees
trees_built = 0
attempts = 0
while trees_built < 45 and attempts < 200:
    rx = center_world_x + random.randint(-forest_radius, forest_radius)
    rz = center_world_z + random.randint(-forest_radius, forest_radius)
    if is_safe_zone(rx, rz):
        build_small_tree(rx, rz)
        trees_built += 1
    attempts += 1

# 5. SYLLABUS SIGNS
mc.postToChat("Placing Syllabus Signs...")
syllabus_data = [
    ["=== PAGE 1 ===", "IT 359", "Pen Testing", "Updated 9/15/25"],
    ["Note:", "Support Hours", "M/W/F", "9 AM - 5 PM"],
    ["Instructor:", "Dr. Sean Sanders", "spsand1@ilstu", "Room: JH 028"],
    ["Class Time:", "12:35-1:50 PM", "Mon / Wed", ""],
    ["Student Support:", "Hours:", "By appointment", ""],
    ["=== PAGE 2 ===", "Overview:", "Pen Testing &", "Ethical Hacking"],
    ["Outcomes 1:", "Malicious vs", "Ethical Hacking", "Frameworks"],
    ["Outcomes 2:", "Data Gathering", "Footprinting", "Enumeration"],
    ["Outcomes 3:", "Intrusions", "Escalate Privs", "Trojans/Exfil"],
    ["Outcomes 4:", "Threat Hunting", "Proactive/Anomaly", "Threat Models"],
    ["Outcomes 5:", "Incident Resp", "Live Analysis", "Malware Analys"],
    ["Knowledge 1:", "Cyber Fundmntls", "Ethics & Diffs", "Offensive Skill"],
    ["Knowledge 2:", "Threat Intel", "Actor Profiles", "IOCs"],
    ["Knowledge 3:", "Incident Resp", "Static/Dynamic", "Analysis"],
    ["=== PAGE 3 ===", "Technology:", "School IT Reqs", "Reliable Net"],
    ["Comm:", "Class Website", "Check Email", "Regularly"],
    ["Contact:", "Email Prof", "Allow time", "for response"],
    ["Textbook/Lab:", "HackTheBox", "VIP+ Sub", "$20 per month"],
    ["=== PAGE 4 ===", "Optional Mats:", "IEEE Security", "ACM Transact"],
    ["Journals:", "Computers & Sec", "Info Sec Jrnl", "Reggienet"],
    ["Format:", "60% Lecture", "40% Lab", "Concepts->Lab"],
    ["=== PAGE 5 ===", "Grading:", "Labs: 40%", "Partic: 10%"],
    ["Grading Cont:", "Project: 20%", "Exams: 30%", "(2 @ 15%)"],
    ["Scoring:", "Out of 100", "Weighted", "No indiv grades"],
    ["=== PAGE 6 ===", "Scale:", "A: 90.00+", "B: 80-89.99"],
    ["Scale Cont:", "C: 70-79.99", "D: 60-69.99", "F: < 59.99"],
    ["PASSING REQ:", "MUST SCORE >60", "IN ALL PARTS", "TO PASS!"],
    ["Failure Ex:", "Lab=40, Rest=90", "result is F", "Must pass all"],
    ["Curving:", "Components:", "NO Curve", "Cutoffs: Maybe"],
    ["=== PAGE 7 ===", "Quizzes:", "Weekly/Canvas", "Start of class"],
    ["Quiz Info:", "10-20 Mins", "Read AHEAD", "of class"],
    ["Exams:", "Includes", "Challenges", ""],
    ["Labs:", "Hands-on Tools", "Submit Canvas", "Strict Deadline"],
    ["Lab Policy:", "Late Work", "NOT Graded", "Canvas Only"],
    ["=== PAGE 8 ===", "Attendance:", "Expected", "Hard to catchup"],
    ["Excused Abs:", "Quarantine", "Death in Fam", "Mil/Jury Duty"],
    ["Not Excused:", "Weddings", "Vacations", "Sports"],
    ["If Excused:", "Notify BEFORE", "Email Prof AND", "Form to Dean"],
    ["Unexcused 1:", "1-2 Misses:", "No Makeups", "No Pts"],
    ["Unexcused 2:", "3 Misses:", "Grade Drop", "Letter Down"],
    ["Unexcused 3:", "4+ Misses:", "Course F", "Fail"],
    ["Lateness:", "Come anyway", "Enter quietly", "No makeup actv"],
    ["=== PAGE 9 ===", "Preparation:", "Read Material", "Before Class"],
    ["Accommodat:", "Student Access", "350 Fell Hall", "309-438-5853"],
    ["Basic Needs:", "Food/Housing", "Contact Dean", "of Students"],
    ["Mental Health:", "SCS Services", "320 Stu Svcs", "309-438-3655"],
    ["MH Support:", "Free/Confid", "Kognito Sim", "Help friends"],
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

current_x = base_x + 5
current_z = base_z + 5
wall_stage = 1 
sign_spacing = 2 

for sign_lines in syllabus_data:
    lines = sign_lines + [""] * (4 - len(sign_lines))
    if wall_stage == 1: 
        mc.setSign(base_x + 4, base_y + 2, current_z, WALL_SIGN, 5, lines[0], lines[1], lines[2], lines[3])
        mc.setBlock(base_x + 4, base_y + 3, current_z, TORCH, 1) 
        current_z += sign_spacing
        if current_z >= base_z + size - 5:
            wall_stage = 2
            current_x += sign_spacing
            current_z = base_z + size - 5 
    elif wall_stage == 2: 
        mc.setSign(current_x, base_y + 2, base_z + size, WALL_SIGN, 2, lines[0], lines[1], lines[2], lines[3])
        mc.setBlock(current_x, base_y + 3, base_z + size, TORCH, 4)
        current_x += sign_spacing
        if current_x >= base_x + size - 5:
            wall_stage = 3
            current_z -= sign_spacing
            current_x = base_x + size - 5 
    elif wall_stage == 3: 
        mc.setSign(base_x + size, base_y + 2, current_z, WALL_SIGN, 4, lines[0], lines[1], lines[2], lines[3])
        mc.setBlock(base_x + size, base_y + 3, current_z, TORCH, 2)
        current_z -= sign_spacing

mc.player.setPos(base_x - 10, base_y + 10, base_z - 10)
mc.postToChat("Construction Complete!")
