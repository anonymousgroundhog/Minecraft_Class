import mcpi.minecraft as minecraft
import mcpi.block as block
import time
import socket

# --- Building Constants ---
WALL_BLOCK = 1       # Stone
LIGHT_BLOCK = 89     # Glowstone 
AIR = 0              # Air 
SIGN_WALL = 68       # Wall Sign
SIGN_DIRECTION = 3   # South-facing (for North interior wall)

# Define building size: 36 blocks wide for 18 signs (18 * 2)
WIDTH = 36
DEPTH = 8
HEIGHT = 4 

# --- Syllabus Content for IT 360 (CLEANED) ---
syllabus_signs_360 = [
    # General Course Info
    ["IT 360", "Security", "Incident", "Forensics"], 
    ["Instructor:", "Dr. S Sanders", "spsand1@ilstu.edu", "Room: JH 030"], 
    ["Time: T/Th", "9:35 AM -", "12:15 PM", ""], 

    # Pre-requisites & Requirements
    ["Pre-reqs:", "C or better", "in IT 276", "& IT 250"], 
    ["Required Text:", "Digital Forensics", "by Easttom", "(4th edition)"], 
    ["Required Labs:", "Cloud Labs", "Course ID:", "A22622"], 

    # Forensics & Analysis Topics
    ["Forensics:", "File Systems", "Data Acq.", "Data Recovery"], 
    ["Analysis:", "OS Artifacts", "Network Logs", "Memory"], 
    ["Specialized:", "Mobile Device", "App Data", "Extraction"], 

    # Investigation & Methodology
    ["Methodology:", "Collect", "Seize", "Protect Evidence"], 
    ["Topics:", "Digital Forensic", "Methodology", "Laws"], 
    ["Course Focus:", "Detecting", "Responding", "Investigating"], 

    # Grading
    ["Grading:", "Labs 40%", "Exams 30%", "Project 20%"], 
    ["Grading:", "Particip 10%", "Total 100%", ""], 
    ["Passing Req:", "Min 60% in", "ALL", "components"], 
    ["Grade C:", "70.00-79.99", "", ""], 

    # Other Policies
    ["Quizzes:", "Weekly on", "Canvas", "Closed Notes"], 
    ["Absence:", "3 missed =", "1 grade", "reduction"], 
    ["Absence:", "4+ missed", "equals", "F for course"], 
]


# --- Building Function ---
def build_syllabus_monument(mc, start_x, start_y, start_z, width, height, depth, sign_list, building_name):
    """Constructs a building with signs and lighting at the specified coordinates."""
    
    mc.postToChat(f"Building {building_name}...")

    # 1. Clear Area (1 block under, 1 block around, 5 blocks high)
    mc.postToChat("Clearing area...")
    mc.setBlocks(start_x - 1, start_y - 1, start_z - 1, start_x + width + 1, start_y + height + 1, start_z + depth + 1, AIR)

    # 2. Build the Floor (Stone)
    mc.setBlocks(start_x, start_y, start_z, start_x + width, start_y, start_z + depth, WALL_BLOCK)

    # 3. Build the Walls (Stone) and Ceiling (Stone)
    ceiling_y = start_y + height
    # North Wall (Interior signs go here)
    mc.setBlocks(start_x, start_y + 1, start_z, start_x + width, ceiling_y - 1, start_z, WALL_BLOCK) 
    # South Wall (Entrance will be here)
    mc.setBlocks(start_x, start_y + 1, start_z + depth, start_x + width, ceiling_y - 1, start_z + depth, WALL_BLOCK) 
    # West Wall
    mc.setBlocks(start_x, start_y + 1, start_z + 1, start_x, ceiling_y - 1, start_z + depth - 1, WALL_BLOCK) 
    # East Wall
    mc.setBlocks(start_x + width, start_y + 1, start_z + 1, start_x + width, ceiling_y - 1, start_z + depth - 1, WALL_BLOCK) 
    # Build the ceiling 
    mc.setBlocks(start_x, ceiling_y, start_z, start_x + width, ceiling_y, start_z + depth, WALL_BLOCK) 

    # 4. Add the Entrance (2 blocks high opening on the South wall)
    door_center_x = start_x + width // 2
    mc.setBlocks(door_center_x, start_y + 1, start_z + depth, door_center_x + 1, start_y + 2, start_z + depth, AIR)
    mc.postToChat("Entrance added to the South wall.")

    # 5. Place the Signs and Lights (Interior North Wall)
    sign_y = start_y + 2       # Signs 2 blocks high on the wall
    light_y = ceiling_y        # Lights placed on the ceiling
    current_x = start_x + 1    # Start 1 block in from the corner

    for sign_text in sign_list:
        # Place the sign on the North wall (Z coordinate) facing South (SIGN_DIRECTION=3)
        mc.setSign(current_x, sign_y, start_z + 1, SIGN_WALL, SIGN_DIRECTION, sign_text[0], sign_text[1], sign_text[2], sign_text[3])
        
        # Place a GLOWSTONE block (ID 89) on the ceiling directly above the sign
        mc.setBlock(current_x, light_y, start_z + 1, LIGHT_BLOCK)
        
        # Move over 2 blocks for the next sign/light
        current_x += 2
        
        # Safety check
        if current_x > start_x + width - 1:
            mc.postToChat("Warning: Ran out of space for all signs on the wall!")
            break

    mc.postToChat(f"{building_name} complete!")
    
    # Return the last x-coordinate used (the far end of the building)
    return start_x + width


# --- IP Address Input ---
def get_server_ip():
    default_ip = "localhost" 
    ip_address = input(f"Enter the Minecraft server IP address (default: {default_ip}): ")
    
    if not ip_address:
        ip_address = default_ip
        
    try:
        # Checks if it's a valid address format
        socket.inet_aton(ip_address)
    except socket.error:
        if ip_address.lower() != "localhost":
             print(f"Warning: '{ip_address}' may not be a valid IP address format.")
             
    return ip_address

# --- Main Execution ---
if __name__ == "__main__":
    
    # --- Connect to Server ---
    server_ip = get_server_ip()
    try:
        mc = minecraft.Minecraft.create(server_ip)
        mc.postToChat("Connected to Minecraft server at " + server_ip)
    except ConnectionRefusedError:
        print("\nERROR: Could not connect to the Minecraft server.")
        print("Please ensure Minecraft is running and the IP address is correct.")
        exit()

    # Get initial position
    player_pos = mc.player.getTilePos()
    start_y = player_pos.y
    
    # --- 1. Build IT 359 Monument ---
    start_x_359 = player_pos.x + 2
    start_z = player_pos.z + 2 # Z coordinate is shared for both buildings (next to player)
    
    # IT 359 Signs (Re-using cleaned list from previous steps)
    syllabus_signs_359 = [
        ["IT 359", "Penetration", "Testing", "Ethical Hacking"],
        ["Instructor:", "Dr. S Sanders", "spsand1@ilstu.edu", "Room: JH 028"],
        ["Time: M/W", "12:35 PM", "- 1:50 PM", ""],
        ["Pre-reqs:", "C or better", "in IT 250", "& IT 276"],
        ["Tech Req:", "School of IT", "standards", ""],
        ["Required Lab:", "HackTheBox", "VIP+", "$20/month"],
        ["Offense:", "Data Gathering", "Footprinting", "Enumeration"],
        ["Offense:", "Perform", "Intrusions", "Escalate Priv."],
        ["Offense:", "Trojans", "Data", "Exfiltration"],
        ["Threat Hunt:", "Proactive", "Detection", "Anomaly"],
        ["Incident", "Response:", "Live System", "Analysis"],
        ["Malware:", "Static &", "Dynamic", "Analysis"],
        ["Grading:", "Labs 40%", "Exams 30%", "Pres/Proj 20%"],
        ["Grading:", "Particip 10%", "Total 100%", ""],
        ["Passing Req:", "Min 60% in", "ALL", "components"],
        ["Grade A:", "90.00 &", "above", ""],
        ["Grade B:", "80.00-89.99", "", ""],
        ["Quizzes:", "Weekly on", "Canvas", "Read before class"],
        ["Absence:", "3 missed =", "1 grade", "reduction"],
        ["Absence:", "4+ missed", "equals", "F for course"],
    ]
    
    end_x_359 = build_syllabus_monument(mc, start_x_359, start_y, start_z, WIDTH, HEIGHT, DEPTH, syllabus_signs_359, "IT 359 Syllabus Monument")
    
    # --- 2. Build IT 360 Monument ---
    # Start 2 blocks after the end of the first building
    start_x_360 = end_x_359 + 2
    
    # syllabus_signs_360 is already defined and cleaned above
    build_syllabus_monument(mc, start_x_360, start_y, start_z, WIDTH, HEIGHT, DEPTH, syllabus_signs_360, "IT 360 Syllabus Monument")
    
    mc.postToChat("Both Syllabus Monuments are complete!")
