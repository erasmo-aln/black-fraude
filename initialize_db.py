import os
import re
from datetime import date

import numpy as np
import pandas as pd
import sqlalchemy
import uuid

import utils
import variables


# Create the engine and connect to the database
engine = sqlalchemy.create_engine(
   f"{variables.RDBMS}://{variables.USERNAME}:{variables.PASSWORD}@{variables.HOST}/{variables.DATABASE}"
   )
con = engine.connect()
