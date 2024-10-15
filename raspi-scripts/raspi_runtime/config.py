# Current configuration of the raspberry pi monitoring scripts

class Config:
  PERF = False  # Turn on performance monitoring
  URL = "http://localhost" # Else like "http://172.26.13.96"

  SECS_PER_IMG = 3

  # MOCKS
  MOCK_MIC = False
  MOCK_SPEAKER = False
  CAMERA_VER = "LAPTOP"
  # NOTE: Can switch to string if we want like "MOCK", "LAPTOP", and "RPI" 
  #  camera versions






