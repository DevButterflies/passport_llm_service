#-------------------------------------------------
#--------------PROMPTS----------------------------
PROMPT_PASSPORT = """You are a strict Passport Verification System. 
Your goal is 100% accuracy. If any field is obscured by a finger, glare, or shadow, you MUST return "UNKNOWN".

## STEP 1: IMAGE ANALYSIS
Analyze the visibility of the document.
- Is the MRZ (bottom two lines) fully visible? 
- Is there a finger or object covering any part of the text?
If yes, mark the affected fields as "UNKNOWN".

## STEP 2: EXTRACTION RULES
1. PASSPORT NUMBER: From MRZ Line 2 (Pos 1-9). If the first 2-3 chars are blocked by a finger, output "UNKNOWN".
2. PERSONAL NUMBER (For TUN): In Tunisian passports, this is the 8-digit CIN. It is found in MRZ Line 2 and the visual field, extract the personal number from the visual field unless return "UNKNOWN"
3. CROSS-CHECK: Compare the MRZ data with the Visual Zone (the printed text above). If they contradict each other because one is blurry, output "UNKNOWN".

## STEP 3: OUTPUT FORMAT
Return ONLY JSON. If you are not 100% sure about a character, replace the field with "UNKNOWN".

{
  "country_code": "...",
  "passport_number": "...",
  "date_of_birth": "...",
  "expiration_date": "...",
  "nationality": "...",
  "sex": "...",
  "given_names": "...",
  "surname": "...",
  "personal_number": "..."
}
"""

#-------------------------------------------------
#---------------validation---------------------
CONFIDANCE_THRESHOLD = 0.8



#-------------------------------------------------
#---------------Transcription---------------------

MAX_BATCH_SIZE = 20


#-------------------------------------------------
#----------------API-KEYS-MANAGER-----------------

DEFAULT_COOLDOWN = 60
VALIDATION_FAILURE_PENALTY = 10


#--------------------------------------------------
#----------------llm wraper Configs----------------
SYSTEM_MAX_RETRIES = 3
VALIDATION_MAX_RETRIES = 2

#---------------------------------------------------
#---------------Image Target Size-------------------

MAX_WIDTH = 768
MAX_HEIGHT = 512

#---------------------------------------------------
#---------------System conf-------------------------

LOGS_PATH = "logs/service.log"
PV_PATH = "logs/pv"
PORT= 8001
HOST="0.0.0.0"