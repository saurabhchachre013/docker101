import sys
import time

if len(sys.argv) < 2:
    print("Usage: python app.py <serves|migrate>")
    sys.exit(1)

arg = sys.argv[1]

if arg == "serves":
    while True:
        print("serving", flush=True)
        time.sleep(2)

elif arg == "migrate":
    print("migrated")
    sys.exit(0)

else:
    print("Invalid argument. Use 'serves' or 'migrate'.")
    sys.exit(1)