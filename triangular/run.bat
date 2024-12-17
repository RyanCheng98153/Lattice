@REM set vars=3 6 9 12 15 18 21 24 27 30 33 36 39 42 

@REM for %%n in (%vars%) do (
@REM     python .\main.py %%n %%n
@REM )

@REM set vars=3 6 9 12 15 18 21 24 27 30 33 36 39 42 

for /L %%n in (3,3,150) do (
    python .\main.py %%n %%n
)

