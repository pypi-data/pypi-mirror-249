import numpy as np
import pandas as pd

# Create a DataFrame for Seaborn
df = pd.DataFrame({
    'Score': np.concatenate([np.random.normal(80, 30, 100), np.random.normal(20, 30, 100)]),
    'Class': ['Class A'] * 100 + ['Class B'] * 100
})

from dream_my_plots import DreamMyPlots
DreamMyPlots(df, """
    📊 Make a plot contains 8 kinds of Distribution Plots (Categorical and Continuous)
    # 🎨 Different classes should have different hues
    🎨 Dark background please, Give a large title please
    🎨 Fit upto 4 subplots horizontally
""", api_key="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")