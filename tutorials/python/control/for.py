# Basic For Loop
for item in list:
    dosomething(item)

# The traditional C for loop has a different form in Python:
for x in range(0, 100):
    dosomething(x)

# More interesting example:
def buglove( UIUC ):
    for bug in UIUC:
        if type( bug ) == type( chinese_lady_beetle() ):
            crush( bug )
        else:
            hug( bug )

