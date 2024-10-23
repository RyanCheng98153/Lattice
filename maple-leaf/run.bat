set vars=49 56 63 70 77 84 91 98 105 112 119 126 133 140

for %%n in (%vars%) do (
    python .\main.py %%n %%n
)


