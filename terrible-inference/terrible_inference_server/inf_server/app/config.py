# File containing configuration settings for webserver

from datetime import timedelta

# TODO: Add settings to know which components should be mocked
class Config:
    # TODO find uses
    ENV = 'CLOUD' # else 'APP'
    OPENAI_KEY = 'blah'

    VECTOR_COSINE = "LIGHT-COMPUTE" # HEAVY-COMPUTE, LIGHT-COMPUTE, DOESNT-RUN, would recc LIGHT-COMPUTE for local
    SIMILARITY_THRESHOLD = 0.70 # 0.75 is good for HEAVY-COMPUTE but 0.7 is probably better for LIGHT-COMPUTE
