from mcpi.minecraft import Minecraft
from mcpi import block
import time

# --- CONNECTION ---
# Use localhost and port 4711
SERVER_IP = "127.0.0.1"
SERVER_PORT = 4711

print(f"Connecting to {SERVER_IP}:{SERVER_PORT}...")
try:
    mc = Minecraft.create(address=SERVER_IP, port=SERVER_PORT)
    pos = mc.player.getTilePos()
    print(f"Connected! Player at {pos.x}, {pos.y}, {pos.z}")
    mc.postToChat("Starting Slow Build...")
except Exception as e:
    print(f"FAILED TO CONNECT: {e}")
    exit()

# --- SETTINGS ---
# We build 5 blocks away from you
sx = pos.x + 5
sy = pos.y
sz = pos.z + 5

WIDTH = 20
HEIGHT = 6
DEPTH = 20

# --- STEP 1: CLEAR THE ZONE ---
print("1. Clearing the area (Bulldozing)...")
mc.setBlocks(sx - 2, sy, sz - 2, sx + WIDTH + 2, sy + HEIGHT + 5, sz + DEPTH + 2, block.AIR.id)
time.sleep(2) # WAIT for server to catch up

# --- STEP 2: BUILD THE SOLID BOX ---
print("2. Building the Solid Stone Box...")
mc.setBlocks(sx, sy, sz, sx + WIDTH, sy + HEIGHT, sz + DEPTH, block.STONE_BRICK.id)

# --- CRITICAL PAUSE ---
# This ensures the stone exists before we try to remove the inside
print("   ... Waiting 2 seconds for server to process stone ...")
time.sleep(2) 

# --- STEP 3: CARVE THE INSIDE (HOLLOW IT OUT) ---
print("3. Carving the Inside (Making it hollow)...")
# We start 1 block IN and end 1 block EARLY
mc.setBlocks(sx + 1, sy + 1, sz + 1, 
             sx + WIDTH - 1, sy + HEIGHT - 1, sz + DEPTH - 1, 
             block.AIR.id)

print("   ... Waiting 1 second ...")
time.sleep(1)

# --- STEP 4: CARVE THE ENTRANCE ---
print("4. Cutting the Door...")
mid_x = sx + (WIDTH // 2)
mc.setBlocks(mid_x, sy + 1, sz, mid_x + 2, sy + 3, sz, block.AIR.id)

# --- STEP 5: BUILD INTERNAL STRUCTURES ---
print("5. Building Internal Room...")
# Inner Room (Solid)
ix, iz = sx + 2, sz + 2
mc.setBlocks(ix, sy, iz, ix + 5, sy + 4, iz + 5, block.WOOD_PLANKS.id)
time.sleep(1) 
# Inner Room (Hollow)
mc.setBlocks(ix + 1, sy + 1, iz + 1, ix + 4, sy + 3, iz + 4, block.AIR.id)
# Inner Room Door
mc.setBlocks(ix + 2, sy + 1, iz, ix + 2, sy + 2, iz, block.AIR.id)

mc.postToChat("Build Complete. Please check if it is hollow.")
print("Done.")
