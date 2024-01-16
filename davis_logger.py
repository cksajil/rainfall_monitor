from gpiozero import Button

rain_sensor = Button(6)
BUCKET_SIZE = 0.2794
count = 0


def bucket_tipped():
    global count
    count += 1


def reset_rainfall():
    global count
    count = 0


rain_sensor.when_pressed = bucket_tipped

# When data is needed to saved
# print(count * BUCKET_SIZE)

# When it is needed to clear
# reset_rainfall()
