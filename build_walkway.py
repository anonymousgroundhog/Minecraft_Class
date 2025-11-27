from mcpi.minecraft import Minecraft
from mcpi import block

# Connect to the server
mc = Minecraft.create("localhost")

# ---------------------------------------------------------
# FULL SYLLABUS TEXT
# ---------------------------------------------------------
# This text includes every section, policy, and detail from the PDF.
full_syllabus_text = """
IT 359: Tools & Techniques in Pen Testing.
Updated: 9/15/2025.
Instructor: Dr. Sean Sanders.
Email: spsand1@ilstu.edu.
Room: Julian Hall 028 (JH 028).
Time: M/W 12:35 PM - 1:50 PM.
Support Hours: By Appt (M/W/F 9-5).

COURSE OVERVIEW:
Catalog: Pen testing and offensive security methodologies with emphasis on ethical hacking.
Prereqs: Grade of C or better in IT 250 and IT 276.

LEARNING GOALS:
1. Discuss diff between malicious hacking and pen testing.
2. Discuss ethical frameworks.
3. Data gathering and footprinting.
4. Enumerate systems.
5. Perform intrusions.
6. Escalate privileges.
7. Trojans and data exfiltration.

THREAT HUNTING:
Proactive detection, Anomaly detection, Threat modeling, Threat actor profiles, IOCs.

INCIDENT RESPONSE:
Live analysis, Malware analysis (static/dynamic), Post-mortem analysis.

REQUIREMENTS:
Computer meeting School of IT specs.
Reliable/fast network.
Check email/website regularly.

TEXTBOOK:
HackTheBox VIP+ Subscription ($20/month).

FORMAT:
60% Lecture / 40% Lab.
Ref: IEEE Security, ACM Privacy, Reggienet.

GRADING WEIGHTS:
Labs: 40%.
Exams: 30% (Midterm & Final).
Project: 20%.
Participation: 10%.
Total: 100%.

GRADING SCALE:
A: 90.00 and above.
B: 80.00 - 89.99.
C: 70.00 - 79.99.
D: 60.00 - 69.99.
F: 59.99 and below.

PASSING REQ:
Must have >60% in ALL components to pass.
Ex: Lab score 40 + Exam 90 = F for course.
No Curving.

ASSESSMENTS:
Quizzes: Weekly, start of class, 10-20 mins. Based on reading.
Exams: Include challenges.
Labs: Hands-on. Submit via Canvas ONLY. No late work accepted.

ATTENDANCE POLICY:
Mandatory.
Excused: Quarantine, Death in family, Military/Jury duty.
(Weddings/Vacations are NOT excused).
Must notify Instructor BEFORE class.

UNEXCUSED ABSENCES:
1-2 missed: No makeup.
3 missed: Letter grade reduction.
4 missed: F for the course.
Lateness: Come in quietly. No makeup for missed activities.

SUPPORT:
Accommodations: Student Access (350 Fell Hall, 309-438-5853).
Basic Needs: Contact Dean of Students.
Mental Health: SCS (320 Student Services, 309-438-3655) - Free/Confidential.

SCHEDULE:
Wk 1-2: Ethical Hacking, Footprinting, Nmap.
Wk 3: Exploits, Privilege Escalation.
Wk 4-8: Red Team, OSINT, Midterm (Mar 8).
Wk 10-16: MITRE ATT&CK, Threat Intel.
Wk 17: Finals, Presentations.
"""

# ---------------------------------------------------------
# HELPER: TEXT WRAPPER
# ---------------------------------------------------------
def create_sign_chunks(text):
    """
    Splits a long string into a list of 4-line chunks 
    that fit on Minecraft signs (~15 chars/line).
    """
    words = text.replace('\n', ' ').split(' ')
    all_lines = []
    current_line = ""

    # Step 1: Wrap text into lines of max 15 chars
    for word in words:
        if len(current_line) + len(word) + 1 <= 15:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
        else:
            all_lines.append(current_line)
            current_line = word
    if current_line:
        all_lines.append(current_line)

    # Step 2: Group lines into chunks of 4 (one sign per chunk)
    sign_chunks = []
    for i in range(0, len(all_lines), 4):
        chunk = all_lines[i:i+4]
        # Fill empty lines if a chunk has fewer than 4
        while len(chunk) < 4:
            chunk.append("")
        sign_chunks.append(chunk)
    
    return sign_chunks

# ---------------------------------------------------------
# MAIN BUILDER
# ---------------------------------------------------------
def place_full_syllabus():
    # Parse the text
    print("Processing text...")
    signs_data = create_sign_chunks(full_syllabus_text)
    print(f"Generated {len(signs_data)} signs.")

    # Get player position
    pos = mc.player.getTilePos()
    start_x = pos.x
    start_y = pos.y
    start_z = pos.z
    
    mc.postToChat(f"Placing {len(signs_data)} signs with full details...")

    # We will build along the X axis
    current_x = start_x + 2
    
    for chunk in signs_data:
        # 1. Place a Dirt Block underneath (to prevent floating signs)
        mc.setBlock(current_x, start_y - 1, start_z, block.DIRT.id)
        
        # 2. Place the Sign (ID 63)
        # 12 = Faces West (towards player if they are at start)
        mc.setBlock(current_x, start_y, start_z, block.SIGN_STANDING.id, 12)
        
        # 3. Write the 4 lines
        mc.setSign(current_x, start_y, start_z, block.SIGN_STANDING.id, 12,
                   str(chunk[0]),
                   str(chunk[1]),
                   str(chunk[2]),
                   str(chunk[3]))
        
        # 4. Spacing: Move 2 blocks forward
        current_x += 2

    # Teleport player to start
    mc.player.setPos(start_x, start_y, start_z)
    mc.postToChat("Syllabus Placed!")

if __name__ == "__main__":
    place_full_syllabus()
