from mcpi.minecraft import Minecraft
from mcpi import block
import time
import random

# --- CONFIGURATION FOR EXTERNAL SERVER (MODIFY THESE) ---
# The MCPI protocol does not use your Minecraft username/password.
# It uses the server's IP address and the RaspberryJuice port (default 4711).
# You must have the RaspberryJuice plugin installed on the external server.
SERVER_IP = "10.110.10.150"
SERVER_PORT = 4711

# --- Connect to Minecraft ---
try:
    # Connects to the external server using the defined IP and Port
    mc = Minecraft.create(SERVER_IP, SERVER_PORT)
    mc.postToChat("Python Script Connected. Starting Campus Build...")
    pos = mc.player.getTilePos()
except Exception as e:
    print(f"Failed to connect to Minecraft server at {SERVER_IP}:{SERVER_PORT}")
    print(f"Error: {e}")
    # Exit gracefully if connection fails
    exit()

# --- Configuration ---
origin_x = pos.x
origin_y = pos.y
origin_z = pos.z

# 1. Main Classroom Building Config
BUILDING_WIDTH = 30
BUILDING_DEPTH = 15
WING_LENGTH = 20
FLOOR_HEIGHT = 5
FLOORS = 3

# 2. QUAD CONFIGURATION
QUAD_LENGTH = 140
QUAD_WIDTH = 100

# 3. Bone Student Center (South End)
BONE_WIDTH = 40
BONE_DEPTH = 25
BONE_START_Z = origin_z + BUILDING_DEPTH + QUAD_LENGTH
BONE_START_X = origin_x + (BUILDING_WIDTH // 2) - (BONE_WIDTH // 2)

# 4. Starbucks
STARBUCKS_WIDTH = 15
STARBUCKS_DEPTH = 15
STARBUCKS_X = BONE_START_X + BONE_WIDTH
STARBUCKS_Z = BONE_START_Z

# 5. Side Classroom Buildings (East & West)
SIDE_HALL_WIDTH = 15
SIDE_HALL_LENGTH = 40
SIDE_HALL_HEIGHT = 15 # 3 stories
# West Building (Left)
WEST_BLDG_X = origin_x - (QUAD_WIDTH // 2) - SIDE_HALL_WIDTH
WEST_BLDG_Z = origin_z + BUILDING_DEPTH + (QUAD_LENGTH // 2) - (SIDE_HALL_LENGTH // 2)
# East Building (Right)
EAST_BLDG_X = origin_x + BUILDING_WIDTH + (QUAD_WIDTH // 2)
EAST_BLDG_Z = WEST_BLDG_Z

# Materials
WALL_MAT = block.BRICK_BLOCK.id
FLOOR_MAT = block.WOOD_PLANKS.id
WINDOW_MAT = block.GLASS_PANE.id
ROOF_MAT = block.STONE_SLAB_DOUBLE.id
COURTYARD_MAT = block.BRICK_BLOCK.id
AIR = block.AIR.id
PILLAR_MAT = block.IRON_BLOCK.id
LIGHT_MAT = block.GLOWSTONE_BLOCK.id
FENCE_MAT = block.FENCE.id
BONE_GLASS_MAT = block.GLASS.id
WALL_SIGN_ID = 68
BONE_ACCENT_MAT = 155
LECTERN_BASE = 85
LECTERN_TOP = 44
GRASS_MAT = block.GRASS.id
LOG_MAT = 17
LEAVES_MAT = 18
PATH_MAT = block.STONE_SLAB_DOUBLE.id

# --- Main Execution ---

def build_campus():
    mc.postToChat("Laying Brick Perimeter...")

    # Calculate Quad Boundaries
    quad_x_min = origin_x + (BUILDING_WIDTH // 2) - (QUAD_WIDTH // 2)
    quad_x_max = origin_x + (BUILDING_WIDTH // 2) + (QUAD_WIDTH // 2)
    quad_z_min = origin_z + BUILDING_DEPTH
    quad_z_max = BONE_START_Z - 1

    # 1. CLEAR LAND
    mc.postToChat("Terraforming...")
    mc.setBlocks(WEST_BLDG_X - 10, origin_y, origin_z - 20,
                 EAST_BLDG_X + SIDE_HALL_WIDTH + 10, origin_y + 50, BONE_START_Z + BONE_DEPTH + 20,
                 AIR)

    # 2. LAY BASE BRICK LAYER (The Perimeter)
    # We fill the ENTIRE campus footprint with brick first.
    # This ensures every building sits on a connected brick surface.
    mc.setBlocks(WEST_BLDG_X - 5, origin_y - 1, origin_z - 5,
                 EAST_BLDG_X + SIDE_HALL_WIDTH + 5, origin_y - 1, BONE_START_Z + BONE_DEPTH + 5,
                 COURTYARD_MAT)

    # 3. LAY GRASS QUAD (The Center)
    # Now we overwrite the center with grass, leaving the brick "border" around the edges
    mc.setBlocks(quad_x_min, origin_y - 1, quad_z_min,
                 quad_x_max, origin_y - 1, quad_z_max,
                 GRASS_MAT)

    # 4. BUILD QUAD PATHS
    build_complex_paths(quad_x_min, quad_x_max, origin_y - 1, quad_z_min, quad_z_max)

    # 5. PLANT TREES
    plant_trees_in_quad(quad_x_min, quad_x_max, origin_y, quad_z_min, quad_z_max)

    # 6. LIGHTING
    mc.postToChat("Lighting the Campus...")
    # Perimeter Lighting (On the brick walk)
    for z in range(quad_z_min, quad_z_max, 15):
        build_light_post(quad_x_min - 2, origin_y, z) # Moved slightly onto the brick
        build_light_post(quad_x_max + 2, origin_y, z) # Moved slightly onto the brick

    # Interior Quad Lighting
    cx = (quad_x_min + quad_x_max) // 2
    cz = (quad_z_min + quad_z_max) // 2
    build_light_post(cx + 5, origin_y, cz + 5)
    build_light_post(cx - 5, origin_y, cz - 5)
    build_light_post(cx + 5, origin_y, cz - 5)
    build_light_post(cx - 5, origin_y, cz + 5)


    # --- BUILDINGS ---

    # A. North: Main Classroom Building
    mc.postToChat("Building Main Hall...")
    build_main_building()

    # B. South: Bone Student Center + Starbucks
    mc.postToChat("Building Student Center...")
    build_bone_center(BONE_START_X, origin_y, BONE_START_Z)
    build_starbucks(STARBUCKS_X, origin_y, STARBUCKS_Z)

    # C. West: Side Classroom Hall
    mc.postToChat("Building West Hall...")
    build_classroom_hall(WEST_BLDG_X, origin_y, WEST_BLDG_Z, SIDE_HALL_WIDTH, SIDE_HALL_LENGTH, "West Hall", door_side="east")

    # D. East: Side Classroom Hall
    mc.postToChat("Building East Hall...")
    build_classroom_hall(EAST_BLDG_X, origin_y, EAST_BLDG_Z, SIDE_HALL_WIDTH, SIDE_HALL_LENGTH, "East Hall", door_side="west")

    mc.postToChat("Campus Upgrade Complete!")

# --- LANDSCAPING FUNCTIONS ---

def build_complex_paths(x1, x2, y, z1, z2):
    cx = (x1 + x2) // 2
    cz = (z1 + z2) // 2

    north_door = (origin_x + BUILDING_WIDTH // 2, origin_z + BUILDING_DEPTH)
    south_door = (BONE_START_X + BONE_WIDTH // 2, BONE_START_Z)
    west_door  = (WEST_BLDG_X + SIDE_HALL_WIDTH, WEST_BLDG_Z + SIDE_HALL_LENGTH // 2)
    east_door  = (EAST_BLDG_X, EAST_BLDG_Z + SIDE_HALL_LENGTH // 2)

    nw = (x1, z1)
    ne = (x2, z1)
    sw = (x1, z2)
    se = (x2, z2)

    # Central Hub
    mc.setBlocks(cx - 4, y, cz - 4, cx + 4, y, cz + 4, PATH_MAT)

    # Axial Paths
    draw_line(cx, cz, north_door[0], north_door[1], y, PATH_MAT, width=3)
    draw_line(cx, cz, south_door[0], south_door[1], y, PATH_MAT, width=3)
    draw_line(cx, cz, west_door[0], west_door[1], y, PATH_MAT, width=3)
    draw_line(cx, cz, east_door[0], east_door[1], y, PATH_MAT, width=3)

    # Diagonal Paths
    draw_line(cx, cz, nw[0], nw[1], y, PATH_MAT, width=2)
    draw_line(cx, cz, ne[0], ne[1], y, PATH_MAT, width=2)
    draw_line(cx, cz, sw[0], sw[1], y, PATH_MAT, width=2)
    draw_line(cx, cz, se[0], se[1], y, PATH_MAT, width=2)

    # Perimeter Path (Between Grass and Brick)
    mc.setBlocks(x1, y, z1, x2, y, z1 + 2, PATH_MAT)
    mc.setBlocks(x1, y, z2 - 2, x2, y, z2, PATH_MAT)
    mc.setBlocks(x1, y, z1, x1 + 2, y, z2, PATH_MAT)
    mc.setBlocks(x2 - 2, y, z1, x2, y, z2, PATH_MAT)

def draw_line(x1, z1, x2, z2, y, block_id, width=1):
    dx = x2 - x1
    dz = z2 - z1
    steps = max(abs(dx), abs(dz))
    if steps == 0: return
    x_inc = dx / steps
    z_inc = dz / steps
    x, z = x1, z1
    for i in range(int(steps)):
        for wx in range(width):
            for wz in range(width):
                mc.setBlock(int(x) + wx, y, int(z) + wz, block_id)
        x += x_inc
        z += z_inc

def plant_trees_in_quad(x1, x2, y, z1, z2):
    for _ in range(100):
        tx = random.randint(x1 + 3, x2 - 3)
        tz = random.randint(z1 + 3, z2 - 3)
        ground_id = mc.getBlock(tx, y - 1, tz)
        if ground_id == GRASS_MAT:
            place_custom_tree(tx, y, tz)

def place_custom_tree(x, y, z):
    leaf_type = random.randint(0, 2)
    height = random.randint(5, 7)
    mc.setBlocks(x-2, y+height-3, z-2, x+2, y+height-2, z+2, LEAVES_MAT, leaf_type)
    mc.setBlocks(x-1, y+height-1, z-1, x+1, y+height, z+1, LEAVES_MAT, leaf_type)
    mc.setBlock(x, y+height+1, z, LEAVES_MAT, leaf_type)
    mc.setBlocks(x, y, z, x, y+height-1, z, LOG_MAT, 0)

# --- BUILDING FUNCTIONS ---

def build_classroom_hall(x, y, z, width, length, name, door_side="east"):
    # Replaces 'build_generic_hall' with a detailed classroom version
    # Note: We don't lay the foundation here anymore because the
    # entire campus foundation is laid in Step 2 of build_campus()

    num_rooms = 4
    room_length = length // num_rooms

    for f in range(FLOORS):
        cy = y + (f * FLOOR_HEIGHT)
        mc.setBlocks(x, cy, z, x + width, cy, z + length, FLOOR_MAT)
        mc.setBlocks(x, cy + FLOOR_HEIGHT, z, x + width, cy + FLOOR_HEIGHT, z + length, ROOF_MAT)
        mc.setBlocks(x, cy + 1, z, x + width, cy + FLOOR_HEIGHT - 1, z + length, WALL_MAT)

        mc.setBlocks(x, cy + 2, z + 2, x, cy + 3, z + length - 2, WINDOW_MAT)
        mc.setBlocks(x + width, cy + 2, z + 2, x + width, cy + 3, z + length - 2, WINDOW_MAT)

        mc.setBlocks(x + 1, cy + 1, z + 1, x + width - 1, cy + FLOOR_HEIGHT - 1, z + length - 1, AIR)

        for i in range(1, num_rooms):
            wall_z = z + (i * room_length)
            mc.setBlocks(x + 1, cy + 1, wall_z, x + width - 1, cy + FLOOR_HEIGHT - 1, wall_z, WALL_MAT)
            mid_x = x + (width // 2)
            mc.setBlocks(mid_x, cy + 1, wall_z, mid_x, cy + 2, wall_z, AIR)

        for i in range(num_rooms):
            rz_center = z + (i * room_length) + (room_length // 2)
            rx_center = x + (width // 2)
            mc.setBlock(rx_center, cy + FLOOR_HEIGHT - 1, rz_center, LIGHT_MAT)
            if door_side == "east":
                mc.setBlock(x + 1, cy + 1, rz_center, LECTERN_BASE)
                mc.setBlock(x + 1, cy + 2, rz_center, LECTERN_TOP)
            else:
                mc.setBlock(x + width - 1, cy + 1, rz_center, LECTERN_BASE)
                mc.setBlock(x + width - 1, cy + 2, rz_center, LECTERN_TOP)

        if f < FLOORS - 1:
            create_stairs(x + 2, cy, z + 2, FLOOR_HEIGHT)
        if f > 0:
            mc.setBlocks(x + 2, cy, z + 2, x + 3, cy, z + 2 + FLOOR_HEIGHT, AIR)
            mc.setBlocks(x + 2, cy + 1, z + 2, x + 3, cy + 3, z + 2 + FLOOR_HEIGHT + 2, AIR)

    mid_z = z + (length // 2)
    if door_side == "east":
        mc.setBlocks(x + width, y + 1, mid_z - 1, x + width, y + 2, mid_z + 1, AIR)
        mc.setSign(x + width + 1, y + 2, mid_z, WALL_SIGN_ID, 5, name)
    elif door_side == "west":
        mc.setBlocks(x, y + 1, mid_z - 1, x, y + 2, mid_z + 1, AIR)
        mc.setSign(x - 1, y + 2, mid_z, WALL_SIGN_ID, 4, name)

def build_main_building():
    for f in range(FLOORS):
        current_y = origin_y + (f * FLOOR_HEIGHT)
        if f == 0:
            center_facing, left_facing, right_facing = 'front', 'right', 'left'
        else:
            center_facing, left_facing, right_facing = 'none', 'none', 'none'

        build_structure(origin_x, current_y, origin_z, BUILDING_WIDTH, BUILDING_DEPTH, rooms=3, door_facing=center_facing)
        build_structure(origin_x, current_y, origin_z + BUILDING_DEPTH, 10, WING_LENGTH, rooms=2, door_facing=left_facing)
        build_structure(origin_x + BUILDING_WIDTH - 10, current_y, origin_z + BUILDING_DEPTH, 10, WING_LENGTH, rooms=2, door_facing=right_facing)

        if f > 0:
             stair_x, stair_z = origin_x + 3, origin_z + 3
             mc.setBlocks(stair_x, current_y, stair_z, stair_x + 1, current_y, stair_z + FLOOR_HEIGHT, AIR)
             mc.setBlocks(stair_x, current_y + 1, stair_z, stair_x + 1, current_y + 3, stair_z + FLOOR_HEIGHT, AIR)
        if f < FLOORS - 1:
             create_stairs(origin_x + 3, current_y, origin_z + 3, FLOOR_HEIGHT)

    door_x = origin_x + (BUILDING_WIDTH // 2)
    mc.setBlocks(door_x - 1, origin_y, origin_z + BUILDING_DEPTH, door_x + 2, origin_y + 2, origin_z + BUILDING_DEPTH, AIR)
    mc.setBlocks(door_x - 2, origin_y, origin_z + BUILDING_DEPTH + 3, door_x - 2, origin_y + 3, origin_z + BUILDING_DEPTH + 3, PILLAR_MAT)
    mc.setBlocks(door_x + 3, origin_y, origin_z + BUILDING_DEPTH + 3, door_x + 3, origin_y + 3, origin_z + BUILDING_DEPTH + 3, PILLAR_MAT)
    mc.setBlocks(door_x - 2, origin_y + 4, origin_z + BUILDING_DEPTH + 1, door_x + 3, origin_y + 4, origin_z + BUILDING_DEPTH + 3, PILLAR_MAT)

def build_structure(x, y, z, width, depth, rooms=1, door_facing='none'):
    mc.setBlocks(x, y, z, x + width, y, z + depth, FLOOR_MAT)
    mc.setBlocks(x, y + FLOOR_HEIGHT, z, x + width, y + FLOOR_HEIGHT, z + depth, ROOF_MAT)
    mc.setBlocks(x, y + 1, z, x + width, y + FLOOR_HEIGHT - 1, z + depth, WALL_MAT)
    mc.setBlocks(x, y + 2, z, x + width, y + 3, z + depth, WINDOW_MAT)
    mc.setBlocks(x + 1, y + 1, z + 1, x + width - 1, y + FLOOR_HEIGHT - 1, z + depth - 1, AIR)
    mc.setBlocks(x, y + 1, z, x, y + FLOOR_HEIGHT - 1, z, WALL_MAT)
    mc.setBlocks(x + width, y + 1, z, x + width, y + FLOOR_HEIGHT - 1, z, WALL_MAT)
    mc.setBlocks(x, y + 1, z + depth, x, y + FLOOR_HEIGHT - 1, z + depth, WALL_MAT)
    mc.setBlocks(x + width, y + 1, z + depth, x + width, y + FLOOR_HEIGHT - 1, z + depth, WALL_MAT)
    room_width = width // rooms
    for i in range(1, rooms + 1):
        curr_room_x_center = x + ((i-1)*room_width) + (room_width // 2)
        curr_room_z_center = z + (depth // 2)
        wall_x = x + (i * room_width)
        if i < rooms:
             mc.setBlocks(wall_x, y + 1, z, wall_x, y + FLOOR_HEIGHT - 1, z + depth, WALL_MAT)
             mc.setBlocks(wall_x, y + 1, z + (depth // 2), wall_x, y + 2, z + (depth // 2), AIR)
        mc.setBlock(curr_room_x_center, y + FLOOR_HEIGHT - 1, curr_room_z_center, LIGHT_MAT)
        if door_facing == 'front': mc.setBlocks(curr_room_x_center, y+1, z+depth, curr_room_x_center, y+2, z+depth, AIR)
        elif door_facing == 'right': mc.setBlocks(x+width, y+1, curr_room_z_center, x+width, y+2, curr_room_z_center, AIR)
        elif door_facing == 'left': mc.setBlocks(x, y+1, curr_room_z_center, x, y+2, curr_room_z_center, AIR)
        if door_facing == 'front' or door_facing == 'none': lx, lz = curr_room_x_center, z + 2
        elif door_facing == 'right': lx, lz = x + 2, curr_room_z_center
        elif door_facing == 'left': lx, lz = x + width - 2, curr_room_z_center
        mc.setBlock(lx, y + 1, lz, LECTERN_BASE)
        mc.setBlock(lx, y + 2, lz, LECTERN_TOP)

def build_bone_center(x, y, z):
    width = BONE_WIDTH
    depth = BONE_DEPTH
    # Note: Foundation is handled in step 2 of build_campus now
    for f in range(FLOORS):
        curr_y = y + (f * FLOOR_HEIGHT)
        for iz in range(depth):
            color = 14 if iz % 2 == 0 else 7
            mc.setBlocks(x, curr_y, z + iz, x + width, curr_y, z + iz, block.WOOL.id, color)
        mc.setBlocks(x, curr_y + FLOOR_HEIGHT, z, x + width, curr_y + FLOOR_HEIGHT, z + depth, ROOF_MAT)
        mc.setBlocks(x, curr_y + 1, z, x + width, curr_y + FLOOR_HEIGHT - 1, z + depth, WALL_MAT)
        mc.setBlocks(x + 4, curr_y + 1, z, x + width - 4, curr_y + FLOOR_HEIGHT - 1, z, BONE_GLASS_MAT)
        mc.setBlocks(x + 1, curr_y + 1, z + 1, x + width - 1, curr_y + FLOOR_HEIGHT - 1, z + depth - 1, AIR)
        for ix in range(x + 5, x + width - 5, 6):
             for iz in range(z + 5, z + depth - 5, 6):
                  mc.setBlock(ix, curr_y + FLOOR_HEIGHT - 1, iz, LIGHT_MAT)
        stair_x = x + width - 5
        stair_z = z + depth - 7
        if f > 0:
             mc.setBlocks(stair_x, curr_y, stair_z, stair_x + 1, curr_y, stair_z + FLOOR_HEIGHT, AIR)
             mc.setBlocks(stair_x, curr_y + 1, stair_z, stair_x + 1, curr_y + 3, stair_z + FLOOR_HEIGHT + 2, AIR)
        if f < FLOORS - 1:
             create_stairs(stair_x, curr_y, stair_z, FLOOR_HEIGHT)
    center_x = x + (width // 2)
    mc.setBlocks(center_x - 3, y + 1, z, center_x + 3, y + 2, z, AIR)
    mc.setBlocks(center_x - 6, y + 4, z - 3, center_x + 6, y + 4, z - 1, BONE_ACCENT_MAT)
    mc.setSign(center_x, y + 4, z - 4, WALL_SIGN_ID, 2, "Bone", "Student", "Center")

def build_starbucks(x, y, z):
    width = STARBUCKS_WIDTH
    depth = STARBUCKS_DEPTH
    mc.setBlocks(x, y, z, x + width, y, z + depth, block.WOOD.id)
    mc.setBlocks(x, y + FLOOR_HEIGHT, z, x + width, y + FLOOR_HEIGHT, z + depth, ROOF_MAT)
    mc.setBlocks(x, y + 1, z, x + width, y + FLOOR_HEIGHT - 1, z + depth, WALL_MAT)
    mc.setBlocks(x + width, y + 2, z + 2, x + width, y + 3, z + depth - 2, BONE_GLASS_MAT)
    mc.setBlocks(x + 2, y + 2, z, x + width - 2, y + 3, z, BONE_GLASS_MAT)
    mc.setBlocks(x, y + 1, z + 1, x + width - 1, y + FLOOR_HEIGHT - 1, z + depth - 1, AIR)
    mc.setBlocks(x, y + 1, z + 1, x, y + FLOOR_HEIGHT - 1, z + depth - 1, BONE_GLASS_MAT)
    door_z = z + 5
    mc.setBlocks(x, y + 1, door_z, x, y + 2, door_z, AIR)
    mc.setSign(x - 1, y + 2, door_z + 1, WALL_SIGN_ID, 4, "Starbucks", "Coffee", "->")
    mc.setBlocks(x + 5, y + 1, z + depth - 4, x + width - 3, y + 1, z + depth - 2, block.STONE.id)
    mc.setBlock(x + 5, y + 2, z + depth - 4, block.TORCH.id)

def create_stairs(x, y, z, height):
    for i in range(height):
        mc.setBlock(x, y + i, z + i, block.STONE_BRICK.id)
        mc.setBlock(x+1, y + i, z + i, block.STONE_BRICK.id)
        mc.setBlocks(x, y + i + 1, z + i, x+1, y + i + 4, z + i + 1, AIR)

def build_light_post(x, y, z):
    mc.setBlock(x, y, z, block.STONE_BRICK.id)
    mc.setBlocks(x, y+1, z, x, y+3, z, FENCE_MAT)
    mc.setBlock(x, y+4, z, LIGHT_MAT)
    mc.setBlock(x, y+5, z, ROOF_MAT)
    mc.setBlock(x+1, y+4, z, WINDOW_MAT)
    mc.setBlock(x-1, y+4, z, WINDOW_MAT)
    mc.setBlock(x, y+4, z+1, WINDOW_MAT)
    mc.setBlock(x, y+4, z-1, WINDOW_MAT)

if __name__ == "__main__":
    time.sleep(2)
    build_campus()
