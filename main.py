import sys
import os
import time
from midi2img import main_midi
from img2midi import main_img
from contextlib import contextmanager,redirect_stderr,redirect_stdout
from os import devnull
from progress.bar import Bar

# Clear log file
open('out.log', 'w').close()

# Suppress warning messages
@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)

# Returns true if song made it to images
def helper(i, images):
    for j in images:
        if i.replace(".mid", "") in j.replace(".png", ""):
            return True

    return False

files = os.listdir("midiFiles")
images = os.listdir("imgOut")
midiOut = os.listdir("midiOut")
midiFinal = os.listdir("midiFinal")

# Cleans up the image directory
if len(images) > 0:
    with Bar('Cleaning directories', max=len(images)+len(midiOut)+len(midiFinal)) as bar:
        for f in images:
            os.remove(f"imgOut/{f}")
            bar.next()
        for f in midiOut:
            os.remove(f"midiOut/{f}")
            bar.next()
        for f in midiFinal:
            os.remove(f"midiFinal/{f}")
            bar.next()

print("\033[032m✓\033[0m Done\n")

# Convert midis to images
bar = Bar('Converting midi files to images', max=len(files))
for i in range(len(files)):
     with suppress_stdout_stderr():
        main_midi(f"midiFiles/{files[i]}", 100)
        bar.next()

bar.finish()

print("\033[032m✓\033[0m Done\n")

# Convert images to midis
images = os.listdir("imgOut")
bar = Bar('Converting filtered images to midi files', max=len(images))
for i in range(len(images)):
    main_img(f"imgOut/{images[i]}", "midiFinal")
    bar.next()

bar.finish()

print("\033[032m✓\033[0m Done\n\nRemoving all redundant files...")

# Removes midis that did not make it to images to save space
for i in files:
    if not helper(i, images):
        print(f" ∘ Removing {i}...")
        os.remove(f"midiFiles/{i}")

print("\033[032m✓\033[0m Done")

if os.stat("out.log").st_size == 0:
    print("out.log updated!")