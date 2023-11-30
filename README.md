# GreetBot

A real-time facial recognition robot.

## Description

GreetBot is a project developed for a club initiative aimed at building a robot capable of greeting people and shaking their hands. The facial recognition component of the project has been extracted into a module that can be utilized for other applications. Please note that the Arduino-related source code is specific to the hardware built for this project, so it will likely need tweaking for other applications.

## Team

- Akshay Gupta
- Angela Liu
- Annie Chen
- Annie Wang
- Christina Pham
- Darren Huai
- Kai Alcayde
- Kenny Wan
- Krish Shah
- Neil Angsanto
- Rudy Orre
- Sally Min
- Sam Chan
- Victoria Ignacio

## Features

### 1. Face Detection

GreetBot's Facial Recognition Module offers powerful face detection capabilities, allowing you to effortlessly determine whether an image contains a face. This feature is perfect for applications that require quick and reliable face presence checks.

```python
from detector import has_face

# Example Usage
if has_face(image):
    print("A face is detected!")
else:
    print("No face found.")
```

### 2. Face Identification

Find and identify the largest face in an image with GreetBot's advanced face identification feature. Retrieve valuable information such as the facial encoding and location for further analysis or interaction.

```python
from detector import find_face

# Example Usage
image, encoding, location = find_face(image)
if encoding is not None:
    print(f"Face found at location: {location}")
else:
    print("No face found.")
```

### 3. Face Encodings Generation

Efficiently generate face encodings and corresponding names from a directory of images using GreetBot's face encodings generation feature. This is particularly useful for applications that require a database of facial information for recognition purposes.

```python

from detector import generate_encodings

# Example Usage
encodings, names = generate_encodings(directory)
print(f"Generated {len(encodings)} face encodings.")
```

## Usage

To use the facial recognition module, include detector.py in your project and import the necessary functions. Example usage can be found in the provided detector.py file.

```python
import cv2
from detector import has_face, find_face, generate_encodings

# Your code here
```

The `generate_encodings()` method is used as a preprocessing step where you can take a directory of face images, and generate a list of encodings which is used by the [dlib](http://dlib.net/) model.

## Project Structure

- `src/detector.py`: Contains the facial recognition module with functions for face detection and encoding generation.
- `src/runner.py`: The main file integrating the facial recognition module with additional functionalities for a greeting robot.

## Getting Started

1. Clone the repository: `git clone https://github.com/your-username/greetbot.git`

2. Install dependencies: `pip install -r requirements.txt`

3. Explore the facial recognition module and integrate it into your project.

## Contributing

If you find a bug, have a feature request, or want to contribute, please open an issue or create a pull request. Your contributions are welcome!

## License

This project is licensed under the MIT License.
