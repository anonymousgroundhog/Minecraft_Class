from mcpi.minecraft import Minecraft
import mcpi.block as block
import time

mc = Minecraft.create()
pos = mc.player.getTilePos()

mc.postToChat("Hello Minecraft World")
mc.postToChat("Welcome to IT 359 and IT 360")
# --- Configuration ---
base_x = pos.x + 5
base_y = pos.y
base_z = pos.z + 5

size = 41            
wall_height = 10    
tower_height = 14   
#material = block.SANDSTONE.id 
material = block.COBBLESTONE.id 

# --- Helper: Build Wall with Machicolations & Battlements ---
def build_wall_segment(x1, z1, x2, z2, orientation):
    # 1. Solid Wall
    mc.setBlocks(x1, base_y, z1, x2, base_y + wall_height, z2, material)
    
    # 2. Overhangs (Machicolations)
    if orientation == 'NS': # North-South running wall
        mc.setBlocks(x1 - 1, base_y + wall_height, z1, x1 - 1, base_y + wall_height, z2, material)
        # Battlements
        for z in range(z1, z2 + 1, 2):
            mc.setBlock(x1 - 1, base_y + wall_height + 1, z, material) 
            mc.setBlock(x2, base_y + wall_height + 1, z, material)      
    else: # East-West running wall
        mc.setBlocks(x1, base_y + wall_height, z1 - 1, x2, base_y + wall_height, z1 - 1, material)
        # Battlements
        for x in range(x1, x2 + 1, 2):
            mc.setBlock(x, base_y + wall_height + 1, z1 - 1, material) 
            mc.setBlock(x, base_y + wall_height + 1, z2, material)      

# --- Helper: Build Corner Tower ---
def build_tower(x, z):
    mc.setBlocks(x, base_y, z, x + 4, base_y + tower_height, z + 4, material)
    mc.setBlocks(x - 1, base_y + tower_height, z - 1, x + 5, base_y + tower_height, z + 5, material)
    # Simple battlements
    for i in range(0, 7, 2):
        mc.setBlock(x - 1 + i, base_y + tower_height + 1, z - 1, material)
        mc.setBlock(x - 1 + i, base_y + tower_height + 1, z + 5, material)
        mc.setBlock(x - 1, base_y + tower_height + 1, z - 1 + i, material)
        mc.setBlock(x + 5, base_y + tower_height + 1, z - 1 + i, material)

mc.postToChat("Building Castle using Gap Method...")

# --- Step 1: Build 4 Corner Towers ---
build_tower(base_x, base_z)
build_tower(base_x + size, base_z)
build_tower(base_x, base_z + size)
build_tower(base_x + size, base_z + size)

# --- Step 2: Build SOLID Walls (West, East, South) ---
# West
build_wall_segment(base_x + 4, base_z + 4, base_x + 4, base_z + size, 'NS')
# East
build_wall_segment(base_x + size, base_z + 4, base_x + size, base_z + size, 'NS')
# South
build_wall_segment(base_x + 4, base_z + size, base_x + size, base_z + size, 'EW')

# --- Step 3: Build the SPLIT North Wall (To leave a gap) ---
center_x = base_x + 4 + ((size - 4) // 2)
gap_width = 4

# Wall Segment A (Left of gap)
build_wall_segment(base_x + 4, base_z + 4, center_x - 2, base_z + 4, 'EW')

# Wall Segment B (Right of gap)
build_wall_segment(center_x + 2, base_z + 4, base_x + size, base_z + 4, 'EW')

# --- Step 4: Build the Gatehouse ADDITIVELY ---
gate_z = base_z + 4
mc.setBlocks(center_x - 3, base_y, gate_z - 2, center_x - 1, base_y + wall_height, gate_z, material)
mc.setBlocks(center_x + 1, base_y, gate_z - 2, center_x + 3, base_y + wall_height, gate_z, material)
mc.setBlocks(center_x - 3, base_y + 5, gate_z - 2, center_x + 3, base_y + wall_height, gate_z, material)
mc.setBlock(center_x - 3, base_y + wall_height + 1, gate_z - 2, material)
mc.setBlock(center_x + 3, base_y + wall_height + 1, gate_z - 2, material)
mc.setBlock(center_x - 1, base_y + wall_height + 1, gate_z - 2, material)
mc.setBlock(center_x + 1, base_y + wall_height + 1, gate_z - 2, material)

# --- Step 5: Force Clear the Air in the Gap ---
mc.setBlocks(center_x - 1, base_y, gate_z - 3, center_x + 1, base_y + 4, gate_z + 1, block.AIR.id)

# --- Step 6: Place "Welcome to IT 360" Sign ---
sign_id = 63 
sign_orientation = 8 
mc.setSign(center_x + 2, base_y, gate_z - 3, sign_id, sign_orientation, 
           "Welcome", "to", "IT 360", "")

mc.postToChat("Digging the moat...")
# ---------------------------------------------------------
# --- FIXED WATER MOAT SECTION ---
# ---------------------------------------------------------
mc.postToChat("Placing Water (ID 9)...")

# Configuration
moat_width = 4
moat_level = base_y - 1 

# Dimensions
min_x = base_x - 1
max_x = base_x + size + 5
min_z = base_z - 1
max_z = base_z + size + 5

# We use the number 9 explicitly for STATIONARY WATER
WATER_ID = 9 

# North
mc.setBlocks(min_x - moat_width, moat_level, min_z - moat_width,
             max_x + moat_width, moat_level, min_z - 1, WATER_ID)

# South
mc.setBlocks(min_x - moat_width, moat_level, max_z + 1,
             max_x + moat_width, moat_level, max_z + moat_width, WATER_ID)

# West
mc.setBlocks(min_x - moat_width, moat_level, min_z,
             min_x - 1, moat_level, max_z, WATER_ID)

# East
mc.setBlocks(max_x + 1, moat_level, min_z,
             max_x + moat_width, moat_level, max_z, WATER_ID)

# Bridge (Wood Planks ID = 5)
mc.setBlocks(center_x - 1, base_y, min_z - moat_width, 
             center_x + 1, base_y, min_z - 1, 5)

mc.player.setPos(center_x, base_y, min_z - moat_width - 2)
mc.postToChat("Done!")
