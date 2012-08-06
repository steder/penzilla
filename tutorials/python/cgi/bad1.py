# Bad:  This will cause your CGI script to not run at all
error = "a string" + 7
# Okay
error = "a string" + str(7)
# Notice how it's just a simple syntax error?
# Run your code through the interpreter before hand to check for these errors.
