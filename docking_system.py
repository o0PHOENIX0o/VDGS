# from picamera2 import Picamera2
# import cv2
# import numpy as np



# # picam2 = Picamera2()
# # config = picam2.create_preview_configuration()
# # picam2.configure(config)
# # picam2.start()



# stream_config = picam2.stream_configuration()
# width = stream_config["size"][0]
# height = stream_config["size"][1]

# #broker = "192.168.0.112"
# broker = "172.16.16.106"
# port = 1883

# middle_factor = 4
# min_contour_area = 100
# running = False
# last_published_position = None


# middle_factor_topic = "settings/middle_factor"
# max_size_topic = "settings/max_size"
# Control = "script/control"
# ESPDisp = 'cameraDisplay'
# positionTopic = "position"

# def connectToMqtt():
#     client.connect(broker, port=port)

# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("Connected to MQTT Broker")
#         client.subscribe(middle_factor_topic)
#         client.subscribe(max_size_topic)
#         client.subscribe(Control)
#     else:
#         print("not Connected to MQTT Broker")
#         connectToMqtt();

# def on_message(client, userdata, message):
#     global middle_factor, min_contour_area,running
#     msg = message.payload.decode()
#     Topic = message.topic
#     print(f"Received message '{msg}' on topic '{Topic}'")
#     if Topic == middle_factor_topic:
#         middle_factor =int(msg)
#     elif Topic == max_size_topic:
#         min_contour_area = int(msg)
#     elif Topic == Control:
#         if msg == 'start':
#             running = True
#         elif msg == 'stop':
#             running = False

#     print(running,"on message")


# client = mqtt.Client("RaspberryPiClient") 
# client.on_connect = on_connect
# client.on_message = on_message

# connectToMqtt();

# lower_red = np.array([0, 100, 100])
# upper_red = np.array([10, 255, 255])


# client.loop_start()

# vid = cv2.VideoCapture(0)

# try:
#     while True:
#         if running:
            
#             middle_portion_width = width // middle_factor

#             side_portion_width = (width - middle_portion_width) // 2

#             frame = picam2.capture_array()
            
#             if frame is None:
#                 print("Failed to capture frame")
#                 continue
            
#             frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
#             hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
#             red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)

#             contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#             # Find the largest contour based on area
#             largest_contour = max(contours, key=cv2.contourArea, default=None)
#             if largest_contour is not None and cv2.contourArea(largest_contour) > min_contour_area:
#                 M = cv2.moments(largest_contour)
#                 if M["m00"] != 0:
#                     cx = int(M["m10"] / M["m00"])
#                     cy = int(M["m01"] / M["m00"])
                      
#                     if cx < side_portion_width:
#                         position = "Left"
#                     elif cx > width - side_portion_width:
#                         position = "Right"
#                     else:
#                         position = "Middle"
                    
#                      # Publish position data only if it's changed
#                     if position != last_published_position:
#                         client.publish(ESPDisp, position)
#                         client.publish(positionTopic, position)
#                         last_published_position = position
                    

#                     cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
#                     cv2.putText(frame, f"{position} Portion", (cx - 50, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

#             cv2.line(frame, (side_portion_width, 0), (side_portion_width, height), (0, 255, 0), 2)
#             cv2.line(frame, (width - side_portion_width, 0), (width - side_portion_width, height), (0, 255, 0), 2)


#             cv2.imshow('Camera Feed with Object Detection', frame)

        
#             if cv2.waitKey(1) & 0xFF == ord('q'):
#                 break
        
#     cv2.destroyAllWindows()
#     picam2.stop()
# except KeyboardInterrupt:
#     client.disconnect()
#     client.loop_stop()
#     picam2.stop()
#     print("Script terminated")






import cv2
import paho.mqtt.client as mqtt
import numpy as np

broker = "172.16.16.102"
port = 1883

middle_factor = 4
min_contour_area = 100
running = False
# running = True


middle_factor_topic = "settings/middle_factor"
max_size_topic = "settings/max_size"
Control = "script/control"
positionTopic = "position"

def connectToMqtt():
    client.connect(broker, port=port)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(middle_factor_topic)
        client.subscribe(max_size_topic)
        client.subscribe(Control)
    else:
        print("not Connected to MQTT Broker")
        connectToMqtt();

def on_message(client, userdata, message):
    global middle_factor, min_contour_area,running
    msg = message.payload.decode()
    Topic = message.topic
    print(f"Received message '{msg}' on topic '{Topic}'")
    if Topic == middle_factor_topic:
        middle_factor =int(msg)
    elif Topic == max_size_topic:
        min_contour_area = int(msg)
    elif Topic == Control:
        if msg == 'start':
            running = True
        elif msg == 'stop':
            running = False

    print(running,"on message")


client = mqtt.Client("RaspberryPiClient")  # You can choose any client ID you like
client.on_connect = on_connect
client.on_message = on_message

connectToMqtt();




cap = cv2.VideoCapture(0)


if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

width = int(cap.get(3))
height = int(cap.get(4))


lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

import matplotlib.pyplot as plt


client.loop_start()

try:
    while True:
        if running:
            
            middle_portion_width = width // middle_factor

            side_portion_width = (width - middle_portion_width) // 2

            ret, frame = cap.read()

            if not ret:
                print("Error: Failed to capture frame.")
                break

            hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            red_mask = cv2.inRange(hsv_frame, lower_red, upper_red)

            contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                area = cv2.contourArea(contour)

                if area > min_contour_area:
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])

                        if cx < side_portion_width:
                            position = "Left"
                        elif cx > width - side_portion_width:
                            position = "Right"
                        else:
                            position = "Middle"
                        
                        client.publish(positionTopic, position)

                        cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                        cv2.putText(frame, f"{position} Portion", (cx - 50, cy - 20),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            cv2.line(frame, (side_portion_width, 0), (side_portion_width, height), (0, 255, 0), 2)
            cv2.line(frame, (width - side_portion_width, 0), (width - side_portion_width, height), (0, 255, 0), 2)


            cv2.imshow('Camera Feed with Object Detection', frame)

        
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    cap.release()
    cv2.destroyAllWindows()
except KeyboardInterrupt:
    client.disconnect()
    client.loop_stop()
    print("Script terminated")