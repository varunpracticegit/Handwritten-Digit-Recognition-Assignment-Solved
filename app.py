# import pygame
# import sys
# from pygame.locals import *
# import numpy as np
# from keras.models import load_model
# import cv2
# from PIL import Image

# WINDOWSIZEX = 640
# WINDOWSIZEY = 480

# BOUNDARYINC = 5
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)
# RED = (255, 0, 0)

# IMAGESAVE = True

# MODEL = load_model("./bestmodel.h5")

# LABELS = {
#     0: "Zero",
#     1: "One",
#     2: "Two",
#     3: "Three",
#     4: "Four",
#     5: "Five",
#     6: "Six",
#     7: "Seven",
#     8: "Eight",
#     9: "Nine"
# }

# # Initialize pygame
# pygame.init()

# FONT = pygame.font.Font("freesansbold.ttf", 18)
# DISPLAYSURF = pygame.display.set_mode((WINDOWSIZEX, WINDOWSIZEY))
# WHITE_INT = DISPLAYSURF.map_rgb(WHITE)
# pygame.display.set_caption("Digit Board")

# iswriting = False

# number_xcord = []
# number_ycord = []

# image_cnt = 1

# PREDICT = True
# while True:

#     for event in pygame.event.get():
#         if event.type == QUIT:
#             pygame.quit()
#             sys.exit()

#         if event.type == MOUSEMOTION and iswriting:
#             xcord, ycord = event.pos
#             pygame.draw.circle(DISPLAYSURF, WHITE, (xcord, ycord), 4, 0)
#             number_xcord.append(xcord)
#             number_ycord.append(ycord)

#         if event.type == MOUSEBUTTONDOWN:
#             iswriting = True

#         if event.type == MOUSEBUTTONUP:
#             iswriting = False

#             number_xcord = sorted(number_xcord)
#             number_ycord = sorted(number_ycord)

#             rect_min_x, rect_max_x = max(number_xcord[0] - BOUNDARYINC, 0), min(WINDOWSIZEX, number_xcord[-1] + BOUNDARYINC)
#             rect_min_Y, rect_max_Y = max(number_ycord[0] - BOUNDARYINC, 0), min(WINDOWSIZEY, number_ycord[-1] + BOUNDARYINC)

#             number_xcord = []
#             number_ycord = []

#             img_arr = np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x, rect_min_Y:rect_max_Y].T.astype(np.float32)

#             if IMAGESAVE:
#                 cv2.imwrite("image" + str(image_cnt) + ".png", img_arr)
#                 image_cnt += 1

#             if PREDICT:
#                 image = cv2.resize(img_arr, (28, 28))
#                 image = np.pad(image, (10, 10), 'constant', constant_values=0)
#                 image = cv2.resize(image, (28, 28)) / 255

#                 label = str(LABELS[np.argmax(MODEL.predict(image.reshape(1, 28, 28, 1)))])

#                 textSurface = FONT.render(label, True, RED, WHITE)
#                 textRecObj = textSurface.get_rect()
#                 textRecObj.left, textRecObj.bottom = rect_min_x, rect_max_Y
#                 DISPLAYSURF.blit(textSurface, textRecObj)

#         if event.type == KEYDOWN:
#             if event.unicode == "n":
#                 DISPLAYSURF.fill(BLACK)

#     pygame.display.update()


import pygame
import sys
from pygame.locals import *
import numpy as np
from keras.models import load_model
import cv2
from PIL import Image
import os
import glob

WINDOWSIZEX = 640
WINDOWSIZEY = 480

BOUNDARYINC = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

IMAGESAVE = True

MODEL = load_model("./bestmodel.h5")

LABELS = {
    0: "0",
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    9: "9"
}

# Get the current script directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# Initialize pygame
pygame.init()

FONT = pygame.font.Font("freesansbold.ttf", 18)
DISPLAYSURF = pygame.display.set_mode((WINDOWSIZEX, WINDOWSIZEY))
WHITE_INT = DISPLAYSURF.map_rgb(WHITE)
pygame.display.set_caption("Digit Board")

iswriting = False

number_xcord = []
number_ycord = []

image_cnt = 1

PREDICT = True

# Create an empty list to store the individual digit images
digit_images = []

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            # Save the combined image of the drawn digits
            if IMAGESAVE and digit_images:
                combined_image_width = len(digit_images) * 28
                combined_image_height = 28

                combined_image = Image.new('L', (combined_image_width, combined_image_height))

                digit_values = []
                for i, img_arr in enumerate(digit_images):
                    image = cv2.resize(img_arr, (28, 28))
                    image = np.pad(image, (10, 10), 'constant', constant_values=0)
                    image = cv2.resize(image, (28, 28)) / 255

                    label = str(LABELS[np.argmax(MODEL.predict(image.reshape(1, 28, 28, 1)))])

                    textSurface = FONT.render(label, True, RED, WHITE)
                    textRecObj = textSurface.get_rect()
                    textRecObj.left = i * 28
                    textRecObj.bottom = combined_image_height

                    DISPLAYSURF.blit(textSurface, textRecObj)

                    combined_image.paste(Image.fromarray(image * 255).convert('L'), (i * 28, 0))

                    digit_values.append(int(label))

                # Create a directory for saving the combined image if it doesn't exist
                images_dir = os.path.join(script_dir, "digit_images")
                os.makedirs(images_dir, exist_ok=True)

                combined_image_path = os.path.join(images_dir, "combined_image.png")
                combined_image.convert('RGB').save(combined_image_path)
                print("Combined image saved successfully!")

                # Save the digit values as a list in a text file
                text_output = ",".join(str(val) for val in digit_values)
                text_file_path = os.path.join(images_dir, "combined_digits.txt")
                with open(text_file_path, 'w') as text_file:
                    text_file.write(text_output)
                print("Combined digits saved as text successfully!")

                # Remove existing individual digit images
                existing_images =glob.glob(os.path.join(images_dir, "digit_*.png"))
                for image_file in existing_images:
                    os.remove(image_file)
                print("Existing individual digit images removed successfully!")

            pygame.quit()
            sys.exit()

        if event.type == MOUSEMOTION and iswriting:
            xcord, ycord = event.pos
            pygame.draw.circle(DISPLAYSURF, WHITE, (xcord, ycord), 4, 0)
            number_xcord.append(xcord)
            number_ycord.append(ycord)

        if event.type == MOUSEBUTTONDOWN:
            iswriting = True

        if event.type == MOUSEBUTTONUP:
            iswriting = False

            number_xcord = sorted(number_xcord)
            number_ycord = sorted(number_ycord)

            rect_min_x, rect_max_x = max(number_xcord[0] - BOUNDARYINC, 0), min(WINDOWSIZEX, number_xcord[-1] + BOUNDARYINC)
            rect_min_Y, rect_max_Y = max(number_ycord[0] - BOUNDARYINC, 0), min(WINDOWSIZEY, number_ycord[-1] + BOUNDARYINC)

            number_xcord = []
            number_ycord = []

            img_arr = np.array(pygame.PixelArray(DISPLAYSURF))[rect_min_x:rect_max_x, rect_min_Y:rect_max_Y].T.astype(np.float32)

            if IMAGESAVE:
                # Create a directory for saving individual images if it doesn't exist
                images_dir = os.path.join(script_dir, "digit_images")
                os.makedirs(images_dir, exist_ok=True)

                # Save the digit image
                digit_image_path = os.path.join(images_dir, f"digit_{image_cnt}.png")
                cv2.imwrite(digit_image_path, img_arr)

                # Increment the image count
                image_cnt += 1

                # Append the digit image to the list
                digit_images.append(img_arr)

            if PREDICT:
                image = cv2.resize(img_arr, (28, 28))
                image = np.pad(image, (10, 10), 'constant', constant_values=0)
                image = cv2.resize(image, (28, 28)) / 255

                label = str(LABELS[np.argmax(MODEL.predict(image.reshape(1, 28, 28, 1)))])

                textSurface = FONT.render(label, True, RED, WHITE)
                textRecObj = textSurface.get_rect()
                textRecObj.left, textRecObj.bottom = rect_min_x, rect_max_Y
                DISPLAYSURF.blit(textSurface, textRecObj)

    pygame.display.update()



