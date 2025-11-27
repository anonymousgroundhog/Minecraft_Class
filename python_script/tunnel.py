import mcpi.minecraft as minecraft
import mcpi.block as block
import time

mc = minecraft.Minecraft.create("localhost")

# --- Blocks ---
STONE_BRICK = 98
WOOD_PLANKS = 5, 1
COBBLESTONE = 4
RAIL = 66
TORCH = 50
AIR = 0
STAIRS_COBBLE = 67
BEDROCK = 7
GLOWSTONE = 89  # Using Glowstone for floor lighting to prevent darkness

# --- Helper: Draw a Safe Box ---
def draw_safe_segment(x, y, z, width, height, length, direction):
    """
    Builds a hollow box (tunnel segment) with absolute safety checks.
    It builds the OUTER SHELL first, then clears the INSIDE.
    """
    # Calculate dimensions
    dx, dz = 0, 0
    if direction == 'z+': dz = 1
    elif direction == 'z-': dz = -1
    elif direction == 'x+': dx = 1
    elif direction == 'x-': dx = -1
    
    # Perpendicular vector for width
    p_dx, p_dz = abs(dz), abs(dx)
    
    # Iterate along the length
    for i in range(length):
        cx = x + (i * dx)
        cz = z + (i * dz)
        cy = y

        # 1. BUILD THE SHELL (The Solid Container)
        # We go from -width to +width, and -1 (floor) to height+1 (ceiling)
        for w in range(-width, width + 1):
            for h in range(-1, height + 2):
                
                # World Bottom Safety Catch
                # If this block is below Y=1, force it to be BEDROCK and stop going down
                if (cy + h) < 1:
                    mc.setBlock(cx + w*p_dx, 0, cz + w*p_dz, BEDROCK)
                    continue
                
                # Determine block type
                blk = STONE_BRICK # Default wall
                if h == -1: blk = COBBLESTONE # Floor
                elif h == height + 1: blk = WOOD_PLANKS # Ceiling
                elif h == height: blk = WOOD_PLANKS # Arch trim
                
                mc.setBlock(cx + w*p_dx, cy + h, cz + w*p_dz, blk)

        # 2. CARVE THE AIR (The Inside)
        # Only clear the inner area, preserving the shell we just built
        # Inner width is width-1
        mc.setBlocks(cx - (width-1)*p_dx, cy, cz - (width-1)*p_dz, 
                     cx + (width-1)*p_dx, cy + height - 1, cz + (width-1)*p_dz, AIR)
        
        # 3. DECORATE (Rail & Lighting)
        # Rail
        mc.setBlock(cx, cy, cz, RAIL)
        
        # Pillars & Torches every 5 blocks
        if i % 5 == 0:
            # Pillars
            mc.setBlocks(cx - (width-1)*p_dx, cy, cz - (width-1)*p_dz, 
                         cx - (width-1)*p_dx, cy+2, cz - (width-1)*p_dz, STONE_BRICK)
            mc.setBlocks(cx + (width-1)*p_dx, cy, cz + (width-1)*p_dz, 
                         cx + (width-1)*p_dx, cy+2, cz + (width-1)*p_dz, STONE_BRICK)
            # Ceiling Beam
            mc.setBlocks(cx - (width-1)*p_dx, cy+height-1, cz - (width-1)*p_dz, 
                         cx + (width-1)*p_dx, cy+height-1, cz + (width-1)*p_dz, STONE_BRICK)
            # Torches
            mc.setBlock(cx - (width-2)*p_dx, cy+2, cz - (width-2)*p_dz, TORCH, 5)
            mc.setBlock(cx + (width-2)*p_dx, cy+2, cz + (width-2)*p_dz, TORCH, 5)

def build_smart_staircase(start_x, start_y, start_z):
    """
    Decides whether to dig down or build flat based on Y level.
    """
    # SAFETY CHECK: Are we on a flat world?
    # If Y is less than 15, we are too close to the void to dig a deep hole.
    if start_y < 15:
        mc.postToChat("Altitude too low! Building Surface Bunker instead.")
        # We will build a small corridor leading slightly down to a surface tunnel
        # Just go down 2 blocks to level out
        target_y = start_y - 2
    else:
        mc.postToChat("Altitude safe. Digging down.")
        target_y = start_y - 12

    current_x, current_y, current_z = start_x, start_y, start_z
    
    # Loop until we reach target depth
    step_count = 0
    while current_y > target_y:
        
        # Hard limit: NEVER dig past Y=3 (Bedrock safety buffer)
        if current_y <= 3:
            mc.postToChat("Hit Bedrock layer! Stopping excavation.")
            break
            
        current_x += 1 # Moving X+ direction
        current_y -= 1
        
        # Build the "Container" for this stair step
        # Floor
        mc.setBlocks(current_x-2, current_y-1, current_z-2, 
                     current_x+2, current_y-1, current_z+2, COBBLESTONE)
        # Walls/Ceiling box
        mc.setBlocks(current_x-2, current_y, current_z-2, 
                     current_x+2, current_y+4, current_z+2, STONE_BRICK)
        # Clear Air for head
        mc.setBlocks(current_x-1, current_y, current_z-1, 
                     current_x+1, current_y+3, current_z+1, AIR)
        
        # Place Stair
        mc.setBlock(current_x, current_y, current_z, STAIRS_COBBLE, 0) # 0 = Ascending East
        
        step_count += 1
        time.sleep(0.05)
        
    return current_x, current_y, current_z

# --- MAIN EXECUTION ---

pos = mc.player.getTilePos()
start_x, start_y, start_z = pos.x, pos.y, pos.z

mc.postToChat("Scanning terrain...")

# 1. Build the smart staircase
bottom_x, bottom_y, bottom_z = build_smart_staircase(start_x, start_y, start_z)

# 2. Create the Hub at the bottom
mc.postToChat("Constructing Hub...")
# Force a massive foundation under the hub so it never floats
mc.setBlocks(bottom_x-6, bottom_y-5, bottom_z-6, bottom_x+6, bottom_y-1, bottom_z+6, COBBLESTONE)
# Build the room
mc.setBlocks(bottom_x-5, bottom_y, bottom_z-5, bottom_x+5, bottom_y+5, bottom_z+5, STONE_BRICK)
mc.setBlocks(bottom_x-4, bottom_y, bottom_z-4, bottom_x+4, bottom_y+4, bottom_z+4, AIR)
# Light
mc.setBlock(bottom_x, bottom_y, bottom_z, GLOWSTONE)

# 3. Branch out (using the safe segment builder)
# Adjust start positions to be outside the hub walls
mc.postToChat("Extending Tunnel Network...")

# North Tunnel
draw_safe_segment(bottom_x, bottom_y, bottom_z + 6, 3, 4, 30, 'z+')

# South Tunnel
draw_safe_segment(bottom_x, bottom_y, bottom_z - 6, 3, 4, 30, 'z-')

# East Tunnel (Continuing from stairs)
draw_safe_segment(bottom_x + 6, bottom_y, bottom_z, 3, 4, 30, 'x+')

mc.postToChat("System Complete. Safe to enter.")
