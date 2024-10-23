set vars=66 72 78 84 90 96 102 108 114 120

for %%n in (%vars%) do (
    python .\main.py %%n %%n
)


