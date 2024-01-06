# What is Yoga-Pose-Checker

Yoga Pose Checker is a python program that determines if the correct yoga pose is being performed.
If the yoga pose is correct, a sound is emitted, and if the pose is incorrect, the sound stops.

The program uses Mediapipe's Pose Landmarker, which recognizes the joints of the person in the image and outputs 33 landmarks.
In this case, the image of the person in the tree pose was loaded as the correct yoga pose and the coordinates of the 33 landmarks were output.
Next, the Euclidean distance between the landmark of the person in the camera and the landmark in the loaded image is calculated, and if the Euclidean distance is less than 1, the system sounds a sound as if the pose is close to the model.

<img src='mediapipe.jpeg' height=350 width=750 >

# How to install Yoga-Pose-Checker
`$ pip install opencv-python`

`$ pip install mediapipe`

`$ pip install numpy`

`$ pip install playsound`

# How to play Yoga-Pose-Checker
Stand in a position where the camera captures your entire body from head to toe and perform yoga poses.