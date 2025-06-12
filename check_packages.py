import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import sys

# Print package locations
print(f"Python executable: {sys.executable}")
print(f"pandas location: {pd.__file__}")
print(f"matplotlib location: {plt.__file__}")
print(f"numpy location: {np.__file__}")
print(f"streamlit location: {st.__file__}")
