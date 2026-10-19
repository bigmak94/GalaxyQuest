# Controls (Meta Quest Touch Plus)

The game still sees a Wii Remote with a Nunchuk attached. The Touch Plus
controllers are mapped onto them like this. The mapping lives in
`updateInput()` in `platform/src/xr/xr_app.cpp`.

| Touch Plus | Wii | In Super Mario Galaxy |
|---|---|---|
| Left thumbstick | Nunchuk stick | Move |
| **A** | A | Jump, talk, confirm. Hold to skip a cutscene or a dialogue |
| **B** | Shake the Remote | Spin |
| **Y** | Shake the Remote | Spin |
| Flick the right controller | Shake the Remote | Spin |
| Flick the left controller | Shake the Nunchuk | Spin, keeping the pointer steady |
| Right trigger | B | Shoot star bits, back/cancel in menus |
| Right controller aim | Pointer | Collect star bits, grab Pull Stars, point at menus |
| Left trigger | Z | Crouch, ground pound, long / backflip jumps (with A) |
| Left grip | C | Put the camera behind Mario |
| Menu (left) | + | Pause menu (one press) |
| X | − | Pause menu (one press) |
| Right stick left / right | D-pad left / right | In the diorama: turn it a step (45°) round Mario, behind a short blink. On the giant screen: turn the game camera around Mario in steps, where the level allows it. Pushing the stick right turns the view to the right; with *Invert camera* off (see the VR settings) it moves the camera to the right instead, as the Wii's D-pad did |
| Right stick up, or click | D-pad up | First-person look (shown on the virtual screen); page up in lists |
| Right stick down | D-pad down | Page down in lists |

Rumble is played on both controllers' haptics.

## Tilt

Rolling the Star Ball and surfing on the Ray steer with the Wii Remote's
tilt. There, the right controller's orientation takes its place:

- **Star Ball:** hold the right controller level (it stands for the Wii
  Remote held straight up, as the sign asks). Tip it down to roll forward,
  raise it to roll back, and roll it left or right to steer.
- **Ray:** hold the right controller level, pointing ahead (the penguin's
  "point your Wii Remote at the screen"), and twist it left or right to
  turn.

Elsewhere, the game sees a Wii Remote held level and still, so aiming the
laser never counts as a shake.

## Pointing

- **In gameplay (diorama):** a laser and reticle show where the right
  controller aims; the game's own cursor is hidden. Star bits, Pull Stars
  and enemies respond to the laser itself, near or far. The reticle swells
  and the controller ticks when the laser touches one. The laser runs on to
  the first surface in its way, or far past Mario into open space. Star
  bits you shoot leave from the controller and fly along the laser to its
  end.
- **On the giant screen:** the game's own star cursor shows where the
  controller points, as with a Wii Remote and a TV; no laser is drawn to
  it. The laser only shows while you point at the VR settings panel.
- **In menus:** the pause menu and yes/no prompts appear on the HUD panel in
  front of you, and the title and file select appear on the virtual screen.
  Point at them directly, the same way you point a Wii Remote at a TV.

## View

- The screen, the diorama and the HUD panel are placed straight ahead of
  where you are and face when the game starts, and again when you put the
  headset back on. To recentre at any time, hold the Meta button on the
  right controller.
- By default the world is at 1/500 scale, with Mario about 1.5 m in front
  of you and 0.8 m below eye level.
- When scenery hides Mario from you, the part between you and him fades
  away until he is in view again.
- Choosing a galaxy in the observatory domes, and the first-person view,
  happen on the virtual screen.

## Skipping cutscenes and dialogues

Hold **A** during a cutscene or a dialogue to skip it. After a moment a ring appears at
the lower right of your view and fills while you keep holding. When it is
full, the cutscene is skipped. If you let go early, the ring drains away and
the cutscene carries on. A short press still advances text as usual.

- Movies, the camera tour when you arrive in a galaxy, and Mario's flight
  into it stop at once, the way the game skips them itself.
- Other cutscenes run to their end at high speed while the view is dark and
  the ring spins. Text boxes are advanced for you. If a cutscene asks a
  yes/no question, skipping stops there so you can answer it.
- A dialogue (talking to a Luma, a Toad and so on, most of which are no
  cutscene) runs to its end the same way, all its pages, not just the one
  on screen; it too stops at a yes/no question.

To skip again, let go of A first. The A you held never reaches the game as
a jump. Holding A from before a cutscene started doesn't count.
`skip_hold` in the comfort settings below sets how long to hold.

## Playing as Luigi

Every save file can be played with Mario or Luigi, a new one included:
you do not need to finish the game with Mario first. On a file's start
screen (the one with **Play This File**, which also follows creating a
file), point at the Mario/Luigi button under the file's details and press
A. The file's bar turns green for Luigi. Mario and Luigi keep separate
progress in the same file; the button switches between them. The file's
icon is your own choice either way (Luigi's is among the icons too).

## Pausing

A single press of X or the Menu button opens the pause menu (on the Wii, +
or - had to be held for a fifth of a second, and not while A or B was held
or during a spin). Where the game does not allow pausing for a moment
(while Mario is being hit, during a screen transition) the menu opens as
soon as it does, up to 1.5 s after the press; during cutscenes it does not
open, as on the Wii.

Opening the system menu or taking the headset off pauses the game. When you
come back during play, the game's pause menu is open.

## VR settings

While the pause menu is open (press the Menu button or X), a VR settings
panel appears to the right of its buttons, slightly turned towards you. Aim
the right controller at it and press A or pull the trigger. It holds every
setting of `petari_vr.ini` (see below) on four tabs: click a tab's name at
the top to open it. **−** and **+** change a value by a step (hold to
repeat), a switch turns with a click anywhere on its row, and **Defaults**
puts the settings of the open tab back to their defaults. A setting that
has no effect as things are (the 3D depth while the 3D is off) is dimmed.

**Screen**

- **Giant screen** (on by default) plays the game on a big 16:9 virtual
  screen from the game's own camera, as on a TV; off, the game is a
  diorama in front of you.
- **Screen distance**: how far away the screen is, 2.5 m to 10 m in steps
  of 0.5 m, 4.5 m by default. Drag the slider or use − and +; the mark
  under the slider is the default. The screen is 5.33 m wide, so it spans
  61 degrees at 4.5 m and 30 degrees (a TV seen from the couch) at 10 m.
- **Passthrough** (off by default) shows your own room around the giant
  screen, through the headset's cameras, instead of the dark. It fades in
  and out as you switch it. It only shows on the giant screen: the diorama
  fills the whole view with the game's world. The headset draws the room on
  every refresh, which takes some of the GPU's time.
- **Stereoscopic 3D** (off by default) shows the giant screen's picture in
  3D: the game is drawn once for each eye, from its own camera moved a
  little to either side. The sky and distant scenery lie far behind the
  screen, Mario stands a little in front of it and the ground before him
  comes out towards you. The HUD, the text and the menus float in front of
  the scene; the pointer's star cursor lies on whatever it points at in the
  scene (and with the menus while you point at those). The switch does
  nothing while the giant screen is off (the diorama is 3D anyway).
- **3D depth** (1.75 by default, 0.25 to 3) is how deep that 3D is. Around
  0.5 the whole scene stays behind the screen, like a window, and the
  effect is slight: a screen 4.5 m away leaves little room for depth behind
  it. More brings Mario and the world out of the screen towards you, which
  is where the depth shows; too much is tiring to look at. The paused scene
  changes as you press, so you can pick by eye. Moving the screen nearer
  deepens it too.
- **3D far depth** (0.95 by default, 0.5 to 1) is how far behind the screen
  the farthest things are drawn: at 1 they look infinitely far away.
- **3D resolution** (0.8 by default, 0.5 to 1) is the size of each eye's
  picture relative to the single one. The GPU draws two pictures of the
  game each frame instead of one, so each is a little smaller; 1 is
  sharpest, but frames come late in busy scenes.

**Diorama**

- **Diorama distance**: how far in front of you Mario stands, 0.6 m to 4 m,
  1.5 m by default (slider, or − and + for 10 cm).
- **Height**: how far below your eyes he stands, 0.8 m by default.
- **World size**: the size of the world, 1.0 by default (1.5 is half as big
  again).
- **Follow smoothing** and **Turn smoothing**: how gently the world follows
  Mario and turns with his gravity (the seconds it takes to close half the
  gap; more is gentler), 0.12 s and 0.35 s by default.
- **Turn vignette**: how much the edges of the view darken while the world
  turns, from 0 (not at all) to 1 (the default).
- **See through scenery** (on by default): scenery that hides Mario from
  you fades away between you and him.
- **Turn with the camera** (off by default): the world turns with the game
  camera as it swings round Mario, as early versions did; off, the world
  keeps its facing and the right stick turns it in steps.

**Picture**

- **Smooth motion** turns SpaceWarp on or off (on by default): with it the
  headset makes the in-between frames from the game's motion, so grass,
  flowers and the ground stay sharp while the view follows Mario; off,
  each game frame is shown twice and moving scenery looks doubled. It
  takes effect at once, to compare.
- **Super resolution** (on by default) hands the world to the headset at the
  size it was rendered and lets Meta Quest Super Resolution scale it to the
  display and sharpen it; off, the app scales it itself (softer). The HUD,
  the pause menu and this panel go to the headset as layers of their own,
  so their text stays sharp either way.
- **FidelityFX CAS** (off by default) sharpens the world with AMD's
  contrast adaptive sharpening as the app puts it into the eye images (and
  scales it up there when Super Resolution is off). **CAS strength** goes
  from 0 (least) to 1 (most), 0.5 by default.
- **Lowest resolution** (0.80 by default) is as far as the game may lower
  its render resolution when the GPU is busy; "Now" shows the resolution it
  renders at. 1.00 is Meta's standard eye size. Higher stays sharper, but
  when the GPU cannot keep up frames come late and the view stutters.
  On the giant screen the same happens to the screen's picture: it is
  drawn at its full size (2048x1152) while the GPU keeps up, and smaller
  when it does not (passthrough and the stereoscopic 3D both take GPU
  time), down to three quarters of this setting: 0.60 of the full size at
  the default, which is still close to what the display can show of a
  screen 4.5 m away. The row then shows the picture's size instead.
- **Highest resolution** (1.60 by default) is as far as it may raise it
  while the GPU has time to spare. Lower it to save battery.
- **Refresh rate**: the display's, among those the headset offers. At
  120 Hz (the default) the game's 60 frames a second fit the display
  exactly; other rates make moving things judder, and SpaceWarp only works
  at 120.
- **High clocks** (on by default) asks the headset for high CPU and GPU
  clock levels; off, the system runs them slower to save battery, and more
  frames come late. It takes effect the next time the app starts.

**Game**

- **Language**: the language of the game's texts, among those your disc
  has: English, French, German, Spanish and Italian on the European disc,
  English, French and Spanish on the American one. English by default. The
  game reads it when it starts, so a change shows the next time you start
  the app (the panel says so until then).
- **Invert camera** (on by default): pushing the right stick to the right
  turns the view to the right, in the diorama and on the giant screen (the
  camera itself goes round Mario to the left). Off, the stick moves the
  camera the way you push it, as the Wii's D-pad did. It only swaps the
  camera's turns: the D-pad's left and right still turn pages the usual
  way.
- **Spin shake strength**: how fast to shake either controller to spin,
  20% to 160% in steps of 10%. Lower values need a gentler shake. The
  default, 100%, keeps the original 2.5 m/s threshold. Drag the slider or
  use − and +; the mark under the slider is the default. Changes apply
  immediately to both controllers; B and Y still spin as usual.
- **Hold A to skip**: how long to hold A to skip a cutscene or a dialogue,
  1 s by default; at 0 ("Off") nothing is skipped.

The paused scene behind the menu changes as you change a setting, so you
can judge it before you carry on. When the menu closes, the settings you
changed are written to `petari_vr.ini` (each as its own line; the rest of
the file stays as it is, and settings you never touched keep following the
defaults).

## Comfort settings

Every setting of the VR settings panel is a line of `petari_vr.ini`, next to
the game data in `/sdcard/Android/data/com.galaxy.quest/files/`. The panel
writes it for you; you can also create or edit it yourself, with any of
these lines. The file is read when the app starts.

```
# Size of the world (1 = default, 1.5 = half as big again)
diorama_scale = 1
# Where Mario stands: metres below your eyes and in front of you (the
# distance can also be set on the VR settings panel in the pause menu)
diorama_height = 0.8
diorama_distance = 1.5
# How quickly the world follows Mario and turns with his gravity (seconds
# to close half the gap; larger is gentler). On a small planet it turns a
# little quicker (at most 115 degrees a second) while the view
# would otherwise sink below Mario's horizon; a sudden change of gravity (a
# gravity switch, a room's wall becoming the floor) happens at once behind a
# short blink instead.
# (seconds to close half the gap; larger is gentler)
follow_smoothing = 0.12
turn_smoothing = 0.35
# Darkening at the edges while the world turns (0 = off, 1 = full)
vignette = 1
# Fade out scenery that hides Mario (0 = off)
cutaway = 1
# Seconds to hold A to skip a cutscene (0 = never skip)
skip_hold = 1
# 1: pushing the right stick right turns the view to the right (the camera
# goes round Mario to the left); 0: the stick moves the camera the way it is
# pushed, as the Wii's D-pad did
invert_camera = 1
# Speed needed to shake either controller to spin, relative to the original
# 2.5 m/s (0.2 to 1.6; 1 = 100%, the default). Lower needs a gentler shake.
spin_shake_strength = 1
# The game's language, among those the disc has: english, french, german,
# spanish or italian on the European disc, english, french or spanish on
# the American one (the Japanese and Korean discs have their own only).
# Read when the game starts.
language = english
# Largest render resolution, relative to the headset's recommended eye
# size (1680x1760 on Quest 3). The resolution rises towards this while the
# GPU has time to spare and drops (down to min_resolution) as soon as
# frames are missed. Lower it to save battery.
resolution = 1.6
# The lowest render resolution (0.5 to 1.25; also on the VR settings panel).
# The giant screen's picture goes down to three quarters of it (0.6 of its
# full 2048x1152) while the GPU cannot keep up.
min_resolution = 0.8
# Display refresh rate in Hz. At 120 the game's 60 frames a second fit
# the display exactly; other rates make moving things judder.
refresh_rate = 120
# Application SpaceWarp (at 120 Hz): the headset synthesizes the refresh
# between two game frames from motion vectors the app gives it, so the
# world moving past (as the view follows Mario) looks sharp instead of
# doubled. 0 shows each game frame twice instead.
space_warp = 1
# Meta Quest Super Resolution: the headset scales the world from its render
# size to the display with an edge-aware filter and sharpening. 0 scales it
# in the app (bilinear).
super_resolution = 1
# AMD FidelityFX CAS (contrast adaptive sharpening) on the world, and its
# strength from 0 (least) to 1 (most).
sharpening = 0
sharpening_strength = 0.5
# Play on a giant 16:9 screen from the game's own camera (1, the default)
# or in the diorama (0), and how far away that screen is, in metres (it is
# 5.33 m wide: 61 degrees across at 4.5 m, 30 degrees at 10 m).
giant_screen = 1
screen_distance = 4.5
# 1 shows your room around the giant screen (the headset's passthrough)
# instead of the dark; 0 is the default
passthrough = 0
# The giant screen in stereoscopic 3D (1; 0, the default, shows both eyes
# the same picture). stereo_depth is how deep it looks (0.25 to 3, "3D
# depth" on the VR settings panel): how far in front of the farthest things
# Mario is drawn, in distances between your eyes; about 0.5 keeps everything
# behind the screen, more brings the world out of it. stereo_far is how far
# apart the farthest things are drawn, in distances between your eyes (0.5
# to 1): at 1 they look infinitely far away, and it cannot be more.
# stereo_resolution is the size of each of the two pictures relative to the
# single one (0.5 to 1): 1 is sharpest but takes the GPU a quarter longer
# than 0.8, and frames come late in busy scenes.
stereo_screen = 0
stereo_depth = 1.75
stereo_far = 0.95
stereo_resolution = 0.8
# The folder of the game's files, as chosen on the setup screen (the app's
# own files/game when there is no such line).
# game_path = /storage/emulated/0/Download/cooked
# 1 turns the diorama with the game camera as it swings round Mario (as
# early versions did); 0 keeps the world's facing, and the right stick
# turns it in 45 degree steps.
turn_with_camera = 0
# Ask the headset for high CPU and GPU clock levels (Meta's SustainedHigh,
# the CPU at 1.92 GHz on Quest 3). 0 leaves the clocks to the system, which
# runs the CPU slower to save battery, and more frames come late.
high_clocks = 1
```

To copy it over: `adb push petari_vr.ini /sdcard/Android/data/com.galaxy.quest/files/`.

## Checking performance

After a session, `tools/app_log.sh` shows the app's log. Every 10 s of
gameplay it contains a line like

```
vr: render scale 1.10-1.25 (now 1.20, 3 changes); eye GPU 5.2 ms avg 6.4 max of 8.3; 2 refreshes missed
```

with the range of render resolutions used, and a line
`vr: the frame loop missed N refreshes (M with its own work late)` whenever
refreshes were missed. Only the misses the frame loop was not late for (the
GPU work overran the refresh) lower the resolution: when the loop's own CPU
work runs late, a lower resolution would not help.

With SpaceWarp on, a line `vr: SpaceWarp: N frames with motion vectors in
the last 10 s, M not to extrapolate` follows every 10 s (about 600 frames,
the game's 60 a second; the frames not to extrapolate are cuts, such as the
fade between the diorama and the virtual screen), and
`adb logcat -s VrApi` shows `FPS=60/120` and `ASW=120, Type=App` (the frames a second shown, the synthesized ones included).
