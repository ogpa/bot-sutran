import datetime
import time
from datetime import timezone
createdupdatedAt = str(datetime.datetime.now(timezone.utc))[
    :-9].replace(" ", "T") + "Z"
# print(createdupdatedAt)

fecha = time.strftime("%Y-%m-%d")
print(fecha)
