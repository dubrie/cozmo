#!/usr/bin/env python3

# Copyright (c) 2016 Anki, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''Go Blue

Make Cozmo sing The Victors and commit to being a University of Michigan fan for life.
'''

import sys
import time

try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install Pillow` to install")

import cozmo
from cozmo.util import degrees

def do_hail(robot):
    robot.move_lift(10.0)
    robot.say_text("Hail").wait_for_completed()
    robot.move_lift(-10.0)
    robot.set_lift_height(0.0).wait_for_completed()

def do_a_spin(robot):
    # turn_in_place takes the quickest path to the provided angle
    # so we need to do 2 180s to complete a full 360 degree spin
    robot.turn_in_place(degrees(180)).wait_for_completed()
    robot.turn_in_place(degrees(180)).wait_for_completed()

def run(sdk_conn):
    '''The run method runs once Cozmo is connected.'''
    robot = sdk_conn.wait_for_robot()

    # bring the lift all the way down to start
    robot.set_lift_height(0.0).wait_for_completed()

    image = Image.open("images/block_m.png")

    # resize to fit on Cozmo's face screen
    resized_image = image.resize(cozmo.lcd_face.dimensions(), Image.NEAREST)

    # convert the image to the format used by the lcd screen
    face_image = cozmo.lcd_face.convert_image_to_screen_data(resized_image, invert_image=False)
    
    do_hail(robot)

    robot.say_text("to the victors valiant").wait_for_completed()

    do_hail(robot)

    robot.say_text("to the conquering heroes").wait_for_completed()

    do_hail(robot)

    do_hail(robot)

    robot.say_text("to Michigan the champions of the west").wait_for_completed()

    do_a_spin(robot)

    duration_s = 5.0
    robot.display_lcd_face_image(face_image, duration_s * 1000.0)
    # Pause for Jabrill Peppers
    time.sleep(duration_s)

if __name__ == '__main__':
    cozmo.setup_basic_logging()

    try:
        cozmo.connect(run)
    except cozmo.ConnectionError as e:
        sys.exit("A connection error occurred: %s" % e)
