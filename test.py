import time

def display_word_with_time(word, delay):
    print(word)
    time.sleep(delay)

index = 0

startup_message = [
"FOUR",
"LET-",
"TER ",
"WORD",
" BY ",
"JEFF",
"HOO-",
"VER.",
"AFT-",
"ER  ",
"RAY-",
"MOND",
"WEIS",
"LING",
"--->",
"    "]

delay_time = 0.6
time.sleep 
print(str(delay_time) + "    " + str(len(startup_message) * delay_time) + " seconds.\n")

for start_word in startup_message:
    display_word_with_time(start_word, delay_time)

print(str(delay_time) + "    " + str(len(startup_message) * delay_time) + " seconds.\n")

