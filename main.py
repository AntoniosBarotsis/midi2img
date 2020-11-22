import sys
import os
import time
from midi2img import main_midi
from img2midi import main_img
from contextlib import contextmanager,redirect_stderr,redirect_stdout
from os import devnull
from progress.bar import Bar

@contextmanager
def suppress_stdout_stderr():
    """A context manager that redirects stdout and stderr to devnull"""
    with open(devnull, 'w') as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)

def helper(i, images):
    for j in images:
        if i.replace(".mid", "") in j.replace(".png", ""):
            return True

    return False

files = os.listdir("midiFiles")
images = os.listdir("imgOut")

with Bar('Cleaning directories', max=len(images)) as bar:
    for f in images:
        os.remove(f"imgOut/{f}")
        bar.next()

print("\033[032m✓\033[0m Done\n")

bar = Bar('Converting midi files to images', max=len(files))
for i in range(len(files)):
     with suppress_stdout_stderr():
        main_midi(f"midiFiles/{files[i]}", 100)
        bar.next()

bar.finish()

print("\033[032m✓\033[0m Done\n")

images = os.listdir("imgOut")
bar = Bar('Converting filtered images to midi files', max=len(images))
for i in range(len(images)):
    main_img(f"imgOut/{images[i]}", "midiFinal")
    bar.next()

bar.finish()

print("\033[032m✓\033[0m Done\n\nRemoving all redundant files...")

for i in files:
    if not helper(i, images):
        print(f" ∘ Removing {i}...")
        os.remove(f"midiFiles/{i}")

print("\033[032m✓\033[0m Done")