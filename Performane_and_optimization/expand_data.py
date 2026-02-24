# import pandas as pd

# # Load original file
# df = pd.read_csv("7817_1.csv")   # change name if needed

# print("Original records:", len(df))

# # Multiply rows
# df_big = pd.concat([df] * 625, ignore_index=True)

# print("New records:", len(df_big))

 # Save to new file
# df_big.to_csv("expanded_1million.csv", index=False)

#  print("File saved successfully!")

import pandas as pd

df = pd.read_csv("expanded_1million.csv")
print("Total records:", len(df))