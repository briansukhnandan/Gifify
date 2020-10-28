import glob
import os
import cv2
import numpy as np

from PIL import Image, ImageOps, ImageDraw, ImageFont
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

'''

sys.argv[1] = Name of video file path (str)
sys.argv[2] = Optional text to add to gif file, will be 'PLACEHOLDER' if no text given. (str)
sys.argv[3] = Starting timestamp, required value (int)
sys.argv[4] = Ending timestamp, required value (int)

'''


def Process_Image(video_file_path, optional_text, starting_timestamp, ending_timestamp,
                  grayscale_option, pencil_sketched_option, flipX_option, flipY_option):

    if pencil_sketched_option:
        print("Pencil sketching is enabled")

    if grayscale_option:
        print("Grayscale")

    # Grabs current frame of subclip file by using .read() in OpenCV library.
    def getFrame(subclip_file, sec, count):

        subclip_file.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames, image = subclip_file.read()

        if hasFrames:
            # Save current frame to media/documents/frames
            cv2.imwrite("media/documents/frames/image"+str(count)+".jpg", image)

        return hasFrames

    # For debugging purposes...
    print("Video file: "+video_file_path)
    print("Optional Text: "+optional_text)
    print("Starting Timestamp: "+starting_timestamp)
    print("Ending Timestamp: "+ending_timestamp)

    # Cut the clip with the user-specified timestamps with FFMPEG.
    ffmpeg_extract_subclip("media/documents/"+video_file_path, int(starting_timestamp), int(ending_timestamp),
                           targetname="media/documents/edited"+str(video_file_path)[-4:])

    subclip_file = cv2.VideoCapture('media/documents/edited.mp4')

    # Initializers for creating array of images from mp4 file.
    total_seconds_passed = 0
    frameRate_of_gif = 0.1
    count = 1
    success = getFrame(subclip_file, total_seconds_passed, count)

    # While we are on a frame that is valid, get the frame at that time.
    # Round to 2 decimal places.
    # Then set success to the next frame which will be checked for validity.
    while success:
        count = count+1
        total_seconds_passed = total_seconds_passed + frameRate_of_gif
        total_seconds_passed = round(total_seconds_passed, 2)
        success = getFrame(subclip_file, total_seconds_passed, count)

    # At this point we now have all of our .jpg images in media/document/frames.
    # We should now append them all as a gif and return.
    gif_frames = []

    # No_of_files refers to number of files in FRAMES_DIR.
    FRAMES_DIR = 'media/documents/frames/'
    No_of_files = len(os.listdir(FRAMES_DIR))

    # This loop is where we will take care of all image modifications.
    for i in range(1, No_of_files):
        current_image = Image.open(FRAMES_DIR+"image"+str(i)+".jpg")

        W, H = current_image.size

        # ALL MODIFICATIONS TO IMAGES GO HERE

        # Check if user specified they want the gif to be grayscale.
        if grayscale_option:
            current_image = ImageOps.grayscale(current_image)

        # This will apply the pencil-sketching filter.
        if pencil_sketched_option:

            # Open image in Python OpenCV.
            img = cv2.imread(FRAMES_DIR + "image" + str(i) + ".jpg")

            # Replace current image with the pencil sketched version.
            cv2.imwrite(FRAMES_DIR + "image" + str(i) + ".jpg", convert_to_pencil_sketch(img))

            # Then open back up with Python PIL.
            current_image = Image.open(FRAMES_DIR + "image" + str(i) + ".jpg")

        # Check if user specified they want the gif to be flipped on the x-axis.
        if flipX_option:
            current_image = ImageOps.flip(current_image)

        # Check if user specified they want the gif to be mirrored on the y-axis.
        if flipY_option:
            current_image = ImageOps.mirror(current_image)

        # Lastly, we add text after all modifications are made.
        # (255, 255, 255) refers to the color White.
        if optional_text != 'PLACEHOLDER':

            current_image = current_image.convert('RGB')

            draw = ImageDraw.Draw(current_image)
            font = ImageFont.truetype('media/fonts/impact.ttf', round(H / 12))

            # Draw the text centered on width, but towards the bottom, similar
            # to internet meme format.
            w, h = draw.textsize(optional_text, font)
            draw.text(((W-w)/2, (2/3)*H + round((1/2)*(1/3)*H)), optional_text, (255, 255, 255), font=font)

        # Now add modified image to gif_frames[].
        gif_frames.append(current_image)

    # The array gif_frames[] should now contain all images that we will
    # concatenate together to form our gif. Perform a .save() on gif_frames[0]
    # and specify parameters.
    gif_frames[0].save('media/documents/edited.gif', format='GIF',
                       append_images=gif_frames[1:], save_all=True,
                       duration=(int(ending_timestamp)-int(starting_timestamp))*25, loop=0)

    # Now delete everything in media/documents/frames
    files = glob.glob(FRAMES_DIR+'*')
    for f in files:
        os.remove(f)


def convert_to_pencil_sketch(img):

    scale_percent = 0.60

    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)

    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    kernel_sharpening = np.array([[-1, -1, -1],
                                  [-1, 9, -1],
                                  [-1, -1, -1]])

    sharpened = cv2.filter2D(resized, -1, kernel_sharpening)

    gray = cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY)
    inv = 255 - gray
    gauss = cv2.GaussianBlur(inv, ksize=(15, 15), sigmaX=0, sigmaY=0)

    def dodgeV2(image, mask):
        return cv2.divide(image, 255 - mask, scale=256)

    pencil_jc = dodgeV2(gray, gauss)

    return pencil_jc