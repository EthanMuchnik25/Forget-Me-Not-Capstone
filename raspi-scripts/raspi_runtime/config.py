# Current configuration of the raspberry pi monitoring scripts

class Config:
    PERF = False  # Turn on performance monitoring
    URL = "http://172.24.156.5:4000" # Else like "http://172.26.13.96"

    CREDS_FILE_PATH = "./creds.txt"
    TOKEN_FILE_PATH = "./token.txt"


    SECS_PER_IMG = 3

    # MOCKS
    MOCK_MIC = False
    MOCK_SPEAKER = False
    CAMERA_VER = "LAPTOP"
    # NOTE: Can switch to string if we want like "MOCK", "LAPTOP", and "RPI" 
    #  camera versions






