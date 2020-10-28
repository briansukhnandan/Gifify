from django.shortcuts import redirect, render

from mimetypes import guess_type
from django.http import HttpResponse, HttpResponseRedirect

from .models import VideoFile
from .forms import VideoFileForm

from .scripts import process_image_opts, process_string

import os


def ui_main_view(request):

    # Initializers
    global_message = ''
    ACCEPTABLE_FORMATS = ['.mp4', '.avi', '.wmv', '.mov']

    # Handle file upload which is a HTTP POST request
    if request.method == 'POST':

        # Create a VideoFileForm object which we defined in forms.py
        form = VideoFileForm(request.POST, request.FILES)
        if form.is_valid():

            # Grab information from the form by using our models defined in models.py.
            vf = VideoFile(docfile=request.FILES['docfile'])
            text_for_gif = VideoFile(optional_text=request.POST['optional_text'])
            starting_timestamp = VideoFile(starting_timestamp=request.POST['starting_timestamp'])
            ending_timestamp = VideoFile(ending_timestamp=request.POST['ending_timestamp'])
            grayscale = VideoFile(grayscale_option=request.POST.get('grayscale_option', False))
            pencil_sketched = VideoFile(pencil_sketched_option=request.POST.get('pencil_sketched_option', False))
            flipX = VideoFile(flipX_option=request.POST.get('flipX_option', False))
            flipY = VideoFile(flipY_option=request.POST.get('flipY_option', False))

            # Ensure video file formats are acceptable.
            if vf.docfile.name[-4:].lower() in ACCEPTABLE_FORMATS:

                VIDEO_FILE_PATH = process_string.process_string(vf.docfile.name)
                STARTING_TIMESTAMP = starting_timestamp.starting_timestamp
                ENDING_TIMESTAMP = ending_timestamp.ending_timestamp
                GRAYSCALE_OPTION = grayscale.grayscale_option
                PENCIL_SKETCHED_OPTION = pencil_sketched.pencil_sketched_option
                FLIP_X_OPTION = flipX.flipX_option
                FLIP_Y_OPTION = flipY.flipY_option

                # Check for invalid characters. Semicolons make the program
                # crash no matter what so throw an error.
                INVALID_CHARS = [";"]
                for ic in INVALID_CHARS:
                    if ic in VIDEO_FILE_PATH:
                        HttpResponseRedirect("/error/")

                # First check, make sure STARTING_TIMESTAMP & ENDING_TIMESTAMP
                # are not negative.
                if int(STARTING_TIMESTAMP) < 0:
                    STARTING_TIMESTAMP = int(STARTING_TIMESTAMP)
                    STARTING_TIMESTAMP = STARTING_TIMESTAMP * -1
                    STARTING_TIMESTAMP = str(STARTING_TIMESTAMP)

                if int(ENDING_TIMESTAMP) < 0:
                    ENDING_TIMESTAMP = int(ENDING_TIMESTAMP)
                    ENDING_TIMESTAMP = ENDING_TIMESTAMP * -1
                    ENDING_TIMESTAMP = str(ENDING_TIMESTAMP)

                # Next check, ensure init time is < ending time.
                if int(STARTING_TIMESTAMP) > int(ENDING_TIMESTAMP):
                    global_message = "The starting timestamp cannot be less than the ending timestamp. " \
                                     "They will be swapped."

                    # Swap STARTING_TIMESTAMP and ENDING_TIMESTAMP
                    tmp = STARTING_TIMESTAMP
                    STARTING_TIMESTAMP = ENDING_TIMESTAMP
                    ENDING_TIMESTAMP = tmp

                # Do a temporary save, will delete later.
                vf.save()

                # If the gif text CharField was left blank, put the parameter
                # for that cmd line argument as "PLACEHOLDER" which means it will
                # be ignored when we go to create the gif.
                if not text_for_gif.optional_text:
                    OPTIONAL_TEXT = 'PLACEHOLDER'

                else:
                    OPTIONAL_TEXT = text_for_gif.optional_text

                # Now perform the image processing tasks using the parameters
                # that were provided from the user's form customization.
                process_image_opts.Process_Image(VIDEO_FILE_PATH, OPTIONAL_TEXT, STARTING_TIMESTAMP, ENDING_TIMESTAMP,
                                                 GRAYSCALE_OPTION, PENCIL_SKETCHED_OPTION, FLIP_X_OPTION, FLIP_Y_OPTION)

                # Finally after we're done remove the .mp4 file to avoid clutter.
                os.remove("media/documents/"+VIDEO_FILE_PATH)

                # Then make an os call to specify edited.gif.
                edited_file_path = os.path.join('media', 'documents', 'edited.gif')

                # Make an HTTPResponse object with our gif file as the contents.
                # Then return it to the user.
                #
                # with open(edited_file_path, 'rb') as f:
                #    response = HttpResponse(f, content_type=guess_type(edited_file_path)[0])
                #    response['Content-Length'] = len(response.content)
                #    return response

                return HttpResponseRedirect("/download/")

            else:
                return HttpResponseRedirect("/error/")


        else:
            global_message = 'An error has occurred.'

    else:
        form = VideoFileForm()  # An empty, unbound form

    # Render list page with the documents and the form
    context = {'form': form, 'message': global_message}
    return render(request, 'list.html', context)

def about_view(request):
    return render(request, 'about.html')

def error_view(request):
    return render(request, 'error.html')

def download_view(request):
    return render(request, 'download.html')
