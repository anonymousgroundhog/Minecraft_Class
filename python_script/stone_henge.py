from mcpi.minecraft import Minecraft
from mcpi import block
import math
import time

# --- Configuration ---
RADIUS = 10         # Radius of the stone circle (distance from center to stone)
NUM_STONES = 12     # Number of upright stones (sarsens)
STONE_HEIGHT = 5    # How tall the sarsens are
STONE_WIDTH = 1     # Width/Depth of the sarsen
STONE_BLOCK = block.STONE.id      # ID 1 for Stone
LINTEL_BLOCK = block.STONE_BRICK.id # ID 98 for Stone Brick (A common choice)

def build_stonehenge_relative():
    """Connects to Minecraft and builds the structure relative to the player's position."""
    
    mc = Minecraft.create()
    
    # 1. Get Player Position for Relative Building
    player_pos = mc.player.getPos()
    
    # Set the center of the structure (X0, Y0, Z0)
    # We use integer coordinates for block placement
    X0 = int(player_pos.x)
    Z0 = int(player_pos.z)
    
    # Y0: Start the base 1 block above the player's current block to ensure it's on the surface
    Y0 = int(player_pos.y) + 1 
    
    print(f"Building Stonehenge centered at your position: ({X0}, {Y0}, {Z0})...")

    # 2. Preparation (Optional: Flatten the area)
    # Clear a 1-block high circle of air around the base for a foundation
    mc.setBlocks(X0 - RADIUS - 2, Y0, Z0 - RADIUS - 2, 
                 X0 + RADIUS + 2, Y0 + STONE_HEIGHT + 2, Z0 + RADIUS + 2, 
                 block.AIR.id)
    # Place a flat stone foundation
    mc.setBlocks(X0 - RADIUS - 2, Y0 - 1, Z0 - RADIUS - 2, 
                 X0 + RADIUS + 2, Y0 - 1, Z0 + RADIUS + 2, 
                 block.STONE_BRICK.id)
    
    stone_positions = []

    # 3. Place the vertical sarsens (upright stones) in a circle
    mc.postToChat("Placing vertical stones...")
    for i in range(NUM_STONES):
        # Angle calculation
        angle = 2 * math.pi * i / NUM_STONES
        
        # Calculate X and Z coordinates on the circle
        x = int(X0 + RADIUS * math.cos(angle))
        z = int(Z0 + RADIUS * math.sin(angle))
        
        # Build a vertical pillar using setBlocks
        mc.setBlocks(x, Y0, z, x + STONE_WIDTH - 1, Y0 + STONE_HEIGHT - 1, z + STONE_WIDTH - 1, STONE_BLOCK)
        stone_positions.append((x, z))
        
        time.sleep(0.1) # Delay for stability

    # 4. Place the horizontal lintels (capping stones)
    mc.postToChat("Placing lintels...")
    lintel_y = Y0 + STONE_HEIGHT
    
    for i in range(NUM_STONES):
        # Get coordinates of the current stone (x1, z1) and the next stone (x2, z2)
        x1, z1 = stone_positions[i]
        x2, z2 = stone_positions[(i + 1) % NUM_STONES] # Wrap around to the first stone
        
        # We place a 1-block high lintel at the top level
        # This draws a line between the top corners of the pillars
        
        # Calculate the direction vector
        dx = x2 - x1
        dz = z2 - z1
        distance = math.sqrt(dx**2 + dz**2)
        
        # Normalize the vector to get unit step
        if distance == 0: continue
            
        step_x = dx / distance
        step_z = dz / distance
        
        # Place blocks along the line
        for step in range(int(distance) + 1):
            lintel_x = int(x1 + step * step_x)
            lintel_z = int(z1 + step * step_z)
            mc.setBlock(lintel_x, lintel_y, lintel_z, LINTEL_BLOCK)
        
        time.sleep(0.1)

    mc.postToChat("Stonehenge construction complete! Check it out.")

# --- Run the function ---
# Uncomment the line below to execute the build!
build_stonehenge_relative()
