from mcpi.minecraft import Minecraft
from mcpi import block
import time

# ==============================================================================
# 1. CONFIGURATION AND INITIAL SETUP
# ==============================================================================

# **IP ADDRESS SETTING**
SERVER_IP = "localhost" 
SERVER_PORT = 4711

# --- BLOCK IDs AND DATA VALUES ---
WOOD_PLANKS = 5              # Planks
WOOD_STAIRS = 53             # Oak Stairs
WOOD_SLAB   = 126            # Wood Slab
FENCE       = 85             # Fence
COBBLE_WALL = 139            # Cobblestone Wall
LANTERN_SUB = 89             # Glowstone (Light source)
CHEST       = 54             # Chest
STONE_BRICK = 98             # Stone Brick
STONE_STAIRS= 109            # Stone Brick Stairs
WATER       = 9
AIR         = 0

# --- CONNECTION ---
try:
    mc = Minecraft.create(address=SERVER_IP, port=SERVER_PORT)
    mc.postToChat("Connected to localhost. Initializing dock build...")
except Exception as e:
    print(f"Failed to connect to Minecraft server at {SERVER_IP}:{SERVER_PORT}")
    print(f"Error: {e}")
    exit()

# Get player position and define the starting coordinates
p = mc.player.getTilePos()
X_PLAYER = p.x
Y_SHORE = p.y
Z_PLAYER = p.z

# Main Dock dimensions
WIDTH = 25
LENGTH = 35

# Main Dock Starting Point (Built off-center to allow bridge alignment)
X_START = X_PLAYER - 12
Y_WATER = Y_SHORE - 1
Z_START = Z_PLAYER + 5

# ==============================================================================
# 2. BUILDING FUNCTIONS
# ==============================================================================

def build_foundation(x, y, z, w, l):
    """Builds the underwater foundation and main deck floor."""
    mc.postToChat("1/5: Building foundation and deck...")
    
    mc.setBlocks(x, y - 1, z, x + w, y - 1, z + l, WOOD_PLANKS)
    mc.setBlocks(x, y, z, x + w, y, z + l, WOOD_PLANKS)
    mc.setBlocks(x, y + 1, z, x + w, y + 10, z + l, AIR)

def build_bridge_entrance(x_player, y_shore, z_player, x_dock_base, z_dock_base):
    """Builds the seamless bridge starting from the player's standing location (no fence)."""
    mc.postToChat("2/5: Creating the seamless bridge entrance...")
    
    BRIDGE_WIDTH = 5
    X_BRIDGE_START = x_player - (BRIDGE_WIDTH // 2) 
    Z_BRIDGE_START = z_player
    Z_BRIDGE_END = z_dock_base
    
    mc.setBlocks(X_BRIDGE_START, y_shore, Z_BRIDGE_START, 
                 X_BRIDGE_START + BRIDGE_WIDTH, y_shore, Z_BRIDGE_END, 
                 WOOD_PLANKS)
    mc.setBlocks(X_BRIDGE_START, y_shore + 1, Z_BRIDGE_START, 
                 X_BRIDGE_START + BRIDGE_WIDTH, y_shore + 5, Z_BRIDGE_END, 
                 AIR)
    
    mc.setBlock(X_BRIDGE_START + (BRIDGE_WIDTH // 2), y_shore + 2, Z_START, LANTERN_SUB)


def build_walkways(x_base, y_base, z_base):
    """Creates the lower, finger-like dock walkways visible in the original photo."""
    mc.postToChat("3/5: Adding small walkways...")

    # Tiered Dock Edge (Slabs on the water surface)
    mc.setBlocks(x_base - 1, y_base, z_base - 1, x_base + WIDTH + 1, y_base, z_base - 1, WOOD_SLAB)
    
    # Central Finger Dock 1 (For small boats/details)
    mc.setBlocks(x_base + 8, y_base, z_base - 10, x_base + 9, y_base, z_base - 2, WOOD_SLAB)
    
    # Central Finger Dock 2 (For small boats/details)
    mc.setBlocks(x_base + 11, y_base, z_base - 10, x_base + 12, y_base, z_base - 2, WOOD_SLAB)
    
    # Small decorative pieces
    mc.setBlock(x_base + 10, y_base, z_base - 4, WOOD_PLANKS)
    mc.setBlock(x_base + 10, y_base, z_base - 3, WOOD_SLAB)


def add_mooring_fingers(x_base, y_base, z_base):
    """Builds dedicated, low-profile mooring fingers for player-placed boats."""
    mc.postToChat("4/5: Adding dedicated mooring fingers for boats...")
    
    # Mooring Finger 1 (On the left side of the main dock)
    FINGER1_X = x_base - 1
    FINGER1_Z = z_base + 8
    
    # Extended Mooring Finger (long and narrow)
    mc.setBlocks(FINGER1_X - 10, y_base, FINGER1_Z, FINGER1_X, y_base, FINGER1_Z + 1, WOOD_SLAB)
    
    # Mooring Post (FENCE/COBBLE_WALL)
    mc.setBlock(FINGER1_X - 1, y_base + 1, FINGER1_Z, FENCE)
    mc.setBlock(FINGER1_X - 9, y_base + 1, FINGER1_Z, FENCE)

    # Mooring Finger 2 (On the right side of the main dock)
    FINGER2_X = x_base + WIDTH + 1
    FINGER2_Z = z_base + 20
    
    # Extended Mooring Finger (long and narrow)
    mc.setBlocks(FINGER2_X, y_base, FINGER2_Z, FINGER2_X + 10, y_base, FINGER2_Z + 1, WOOD_SLAB)
    
    # Mooring Post 
    mc.setBlock(FINGER2_X + 1, y_base + 1, FINGER2_Z, FENCE)
    mc.setBlock(FINGER2_X + 9, y_base + 1, FINGER2_Z, FENCE)


def build_taller_house(x, y, z):
    """Builds the left, two-story wooden structure."""
    
    H_WALL = 6
    W_HOUSE = 6
    
    mc.setBlocks(x, y + 1, z, x + W_HOUSE, y + H_WALL, z + W_HOUSE, WOOD_PLANKS)
    mc.setBlocks(x + 1, y + 1, z + 1, x + W_HOUSE - 1, y + H_WALL - 1, z + W_HOUSE - 1, AIR)
    mc.setBlocks(x, y + 4, z, x + W_HOUSE, y + 4, z + W_HOUSE, WOOD_PLANKS)
    mc.setBlocks(x, y + 5, z, x + W_HOUSE, y + 5, z, FENCE)
    mc.setBlocks(x, y + 5, z + W_HOUSE, x + W_HOUSE, y + 5, z + W_HOUSE, FENCE)
    mc.setBlocks(x, y + H_WALL + 1, z, x + W_HOUSE, y + H_WALL + 1, z + W_HOUSE, WOOD_SLAB)
    mc.setBlock(x, y + 1, z + 3, AIR)


def build_stone_roof_house(x, y, z):
    """Builds the right, short, white-roofed structure."""
    
    H_WALL = 3
    W_HOUSE = 8

    mc.setBlocks(x, y + 1, z, x + W_HOUSE, y + H_WALL, z + W_HOUSE, WOOD_PLANKS)
    mc.setBlocks(x + 1, y + 1, z + 1, x + W_HOUSE - 1, y + H_WALL - 1, z + W_HOUSE - 1, AIR)

    Y_ROOF = y + H_WALL + 1
    
    mc.setBlocks(x - 1, Y_ROOF, z - 1, x + W_HOUSE + 1, Y_ROOF, z + W_HOUSE + 1, STONE_BRICK)
    mc.setBlocks(x - 1, Y_ROOF + 1, z - 1, x + W_HOUSE + 1, Y_ROOF + 1, z - 1, STONE_STAIRS, 2)
    mc.setBlocks(x - 1, Y_ROOF + 1, z + W_HOUSE + 1, x + W_HOUSE + 1, Y_ROOF + 1, z + W_HOUSE + 1, STONE_STAIRS, 3)
    mc.setBlocks(x + 1, Y_ROOF + 1, z + 2, x + W_HOUSE - 1, Y_ROOF + 1, z + W_HOUSE - 2, STONE_BRICK)


def add_lighting_and_railings(x_base, y_base, z_base):
    """Adds the final details: lanterns, posts, and perimeter railings."""
    mc.postToChat("5/5: Adding final details...")

    # Perimeter Fences (Railings around the main deck)
    Y_RAIL = y_base + 1
    mc.setBlocks(x_base, Y_RAIL, z_base, x_base + WIDTH, Y_RAIL, z_base, FENCE)
    mc.setBlocks(x_base, Y_RAIL, z_base + LENGTH, x_base + WIDTH, Y_RAIL, z_base + LENGTH, FENCE)
    mc.setBlocks(x_base, Y_RAIL, z_base, x_base, Y_RAIL, z_base + LENGTH, FENCE)
    mc.setBlocks(x_base + WIDTH, Y_RAIL, z_base, x_base + WIDTH, Y_RAIL, z_base + LENGTH, FENCE)

    # Lighting Posts 
    Y_POST_TOP = y_base + 4
    
    mc.setBlocks(x_base + 10, y_base + 1, z_base + 8, x_base + 10, y_base + 3, z_base + 8, COBBLE_WALL)
    mc.setBlock(x_base + 10, Y_POST_TOP, z_base + 8, LANTERN_SUB)
    
    mc.setBlocks(x_base + 20, y_base + 1, z_base + 25, x_base + 20, y_base + 3, z_base + 25, COBBLE_WALL)
    mc.setBlock(x_base + 20, Y_POST_TOP, z_base + 25, LANTERN_SUB)
    
    # Decor (Chests)
    mc.setBlock(x_base + 1, y_base + 1, z_base + 1, CHEST)
    mc.setBlock(x_base + 23, y_base + 1, z_base + 33, CHEST)
    
# ==============================================================================
# 3. EXECUTION
# ==============================================================================

time.sleep(2)

# Execute all build functions
build_foundation(X_START, Y_WATER, Z_START, WIDTH, LENGTH)
build_bridge_entrance(X_PLAYER, Y_SHORE, Z_PLAYER, X_START, Z_START)
build_walkways(X_START, Y_WATER, Z_START)
add_mooring_fingers(X_START, Y_WATER, Z_START) # NEW FUNCTION FOR MOORING

HOUSE1_X = X_START + 2
HOUSE1_Z = Z_START + 22
build_taller_house(HOUSE1_X, Y_WATER, HOUSE1_Z)

HOUSE2_X = X_START + 14
HOUSE2_Z = Z_START + 10
build_stone_roof_house(HOUSE2_X, Y_WATER, HOUSE2_Z)

add_lighting_and_railings(X_START, Y_WATER, Z_START)

mc.postToChat("Complete Dock with functional Mooring Fingers has been built!")
