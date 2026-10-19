> **Disclaimer: this project is 100% made by AI.** All of GalaxyQuest,
> its code, the changes it makes to the decompilation, its tools and this
> documentation, was written by AI: Claude Opus 5.5 with Max thinking, in
> Claude Code. The Super Mario Galaxy decompilation it is built on is the
> work of the people of the Petari team.

<p align="center">
  <img src="docs/images/cover.jpg" alt="GalaxyQuest: a spiral galaxy" width="380">
</p>

# GalaxyQuest

**Play Super Mario Galaxy in virtual reality, natively on Meta Quest 2 and 3.**

Mario's universe becomes a living diorama in front of you: planets float at
arm's length, you lean in to look around them, and you aim at star bits with
your own hand. If you prefer the original camera, the whole game also plays
on a giant virtual screen, just like on a TV.

This is a **native port, not an emulator**. The game's own code, recreated
in C++ by the [Petari decompilation project](https://github.com/SMGCommunity/Petari),
is compiled for the headset's processor. A new platform layer stands in for
the Wii's hardware (graphics, sound, controllers, saves) and presents the
game in VR through OpenXR.

![Mario on a pirate ship in the diorama view](docs/images/diorama.jpg)

> **You need your own copy of Super Mario Galaxy.** Neither this repository
> nor the app contains any game data. You convert your own disc once (its
> files, and the few pieces of data its program holds), copy the result to
> the headset, and the app reads it from there.

## What's different from the Wii version

| | On the Wii | In this port |
|---|---|---|
| Presentation | TV picture from the game camera | A 3D diorama in front of you, or a giant 16:9 virtual screen |
| Picture | 640x456 at 60 frames a second | Each eye rendered at about the headset's own resolution (it adapts to the load), shown at 120 Hz |
| Pointing | Wii Remote pointer on the TV | A laser from the right controller that reaches into the world |
| Spin | Shake the Wii Remote | B or Y, or a flick of either controller |
| Star Ball and Ray | Tilt the Wii Remote | Tilt the right controller |
| Cutscenes and dialogues | Skippable in some places | Hold A to skip any cutscene or a whole dialogue |
| Luigi | After collecting all 120 stars | On any save file from the start |
| Miis | Can be save file icons | Not available: pick one of the game's icons |

**The diorama.** Each level is shown at 1/500 scale on an invisible
tabletop, with Mario about 1.5 m in front of you and a little below eye
level. The world follows him smoothly and turns with his gravity, so he
always stands upright, even when running round a tiny planet. You look
around with your own head, and the right stick turns the view in 45 degree
steps. When a wall comes between you and Mario, the part in the way fades
out. Galaxy intros, launch star flights and a few special views play on a
big virtual screen, and the pause menu and the HUD float on a panel in front
of you.

**The giant screen.** The game starts on a giant 16:9 screen, from the
game's own camera, as it did on a TV; switch *Giant screen* off in the VR
settings (next to the pause menu) for the diorama. The settings panel also
sets how far away the screen is: 4.5 m by default, farther for a TV seen
from the couch, nearer for a cinema. Switch *Stereoscopic 3D* on there and
each eye gets its own picture, as in a 3D cinema: the game's world gets
real depth, far behind the screen and out in front of it (*3D depth* sets
how much). Switch *Passthrough* on to see your own room around the screen
instead of the dark.

**Comfort.** Turning happens in steps behind a short blink, sudden changes
of gravity also happen behind a blink, and the edges of the view darken
while the world turns. How far away Mario stands, how quickly the world
follows him, which way the right stick turns the camera and more can be set
on the VR settings panel: see [docs/CONTROLS.md](docs/CONTROLS.md).

**Languages.** The game plays in any language your disc has (English,
French, German, Spanish or Italian on the European disc; English, French or
Spanish on the American one): pick it on the *Game* tab of the VR settings.

**Picture and smoothness.** The headset runs at 120 Hz with Meta's
Application SpaceWarp, the resolution adapts to the load, and Meta Quest
Super Resolution (plus optional AMD FidelityFX CAS sharpening) keeps the
picture crisp. The HUD, menus and texts are separate layers, sharp at any
resolution.

**Everything else is the original game.** Levels, physics, enemies, music,
story and saves all come from the game's own code and your own game files.

![The pause menu with the VR settings panel](docs/images/pause_settings.jpg)

## What you need

- A **Meta Quest 2 or 3** (both tested and working; a Quest 3S should work
  too but is untested) with
  about 7 GB free, and a **USB-C data cable** to connect it to the computer
  (a charge-only cable does not work).
- **Your Super Mario Galaxy disc**, dumped as an ISO, RVZ or WBFS image (for
  example with [CleanRip](https://wiibrew.org/wiki/CleanRip) on a Wii), or
  already extracted. The European (RMGP01) and American (RMGE01) discs are
  tested; the Japanese and Korean ones have not been tried yet.
- A **computer** with about 16 GB free (10 GB if your disc is already
  extracted). The installer runs on **Windows**; macOS and Linux users can
  follow the [manual installation steps](#installing-manually) below.
- The [**Windows installer**](https://github.com/bigmak94/GalaxyQuest/releases/latest/download/GalaxyQuest-Installer-windows-x86_64.exe)
  from the [latest release](https://github.com/bigmak94/GalaxyQuest/releases/latest).
  It includes the APK, converter, Python, DolphinTool and adb, so no separate
  downloads or terminal commands are needed.

## Installing

### Windows installer (recommended)

1. **Enable developer mode** on the headset, connect it to your computer
   with a USB data cable, and allow USB debugging in the headset. Follow
   [step 1 below](#1-turn-on-developer-mode-on-the-headset) or
   [Meta's setup guide](https://developers.meta.com/horizon/documentation/android-apps/enable-developer-mode).
2. Download and open
   [`GalaxyQuest-Installer-windows-x86_64.exe`](https://github.com/bigmak94/GalaxyQuest/releases/latest/download/GalaxyQuest-Installer-windows-x86_64.exe).
3. Click **Browse** and select your own Super Mario Galaxy ISO, RVZ or WBFS
   image. If you have already extracted the disc, select **Use an already
   extracted folder** and choose that folder or its `DATA` folder.
4. Select your headset if several devices are connected, then click
   **Install**. The installer extracts the disc, converts the game files,
   installs the app and copies the files to the headset. Movies are included
   by default, and temporary files are cleaned up automatically.
5. When installation finishes, put on the headset and open
   **Library > Unknown Sources > GalaxyQuest**.

Allow half an hour, most of it waiting for files to copy. For more details,
logs and installer build instructions, see
[docs/DESKTOP_INSTALLER.md](docs/DESKTOP_INSTALLER.md).

## Installing manually

If you prefer not to use the installer, or use macOS or Linux, follow the
original steps below. You need three free programs on your computer:

- [Python 3.8 or newer](https://www.python.org/downloads/), which runs
  the converter;
- [adb](https://developer.android.com/tools/releases/platform-tools), the
  Android *platform-tools*, which talks to the headset (a zip to unpack,
  nothing to install);
- [Dolphin](https://dolphin-emu.org/), which extracts the disc.

You also need the two downloads of the
[latest release](https://github.com/bigmak94/GalaxyQuest/releases/latest):

- [`GalaxyQuest.apk`](https://github.com/bigmak94/GalaxyQuest/releases/latest/download/GalaxyQuest.apk),
  the app;
- [`GalaxyQuest-converter.zip`](https://github.com/bigmak94/GalaxyQuest/releases/latest/download/GalaxyQuest-converter.zip),
  the Python scripts (`.py` files) that convert your game files and copy
  them to the headset.

> **You do not need to download or clone this repository.** Every Python
> file the steps below use is in `GalaxyQuest-converter.zip`, on the release
> page of this repository. (They are the ones under `tools/` here: if you
> did clone the repository, run the same commands from its root.)

In short: turn on developer mode, install the app, extract your disc,
convert it, copy the result to the headset. Allow half an hour, most of it
waiting for files to copy.

> **Which Python command?** The steps below write `python`. Type what your
> system uses instead:
>
> - **Windows: `py`** (for example `py tools/cook/cook.py ...`). `python`
>   often does nothing there, or opens the Microsoft Store.
> - **macOS and Linux: `python3`**.

### 1. Turn on developer mode on the headset

Developer mode lets the headset run apps that do not come from the store.
It is turned on from your phone, once:

1. You need a free Meta developer account, made with the Meta account
   your headset uses (Meta asks you to verify the account). Meta's page
   linked below shows how.
2. Open the **Meta Horizon** app on your phone, tap the headset icon, tap
   your headset at the top, then **Headset Settings**, **Developer Mode**,
   and switch it on.
3. Connect the headset to the computer with the USB cable and put it on.
   When it asks to **allow USB debugging**, choose *Always allow from this
   computer*.

Meta's own page for this, with pictures:
[Enable developer mode](https://developers.meta.com/horizon/documentation/android-apps/enable-developer-mode).

### 2. Put everything in one folder

1. Unzip `GalaxyQuest-converter.zip`. You get a folder,
   `GalaxyQuest-converter`, with a `tools` folder and a `README.txt` in it.
   Everything below happens in this folder.
2. Move `GalaxyQuest.apk` into it.
3. Get **adb**, the program that talks to the headset. It is part of
   Google's *SDK Platform-Tools*, a free zip of about 10 MB with nothing to
   install. Download the one for your computer:
   - [Windows](https://dl.google.com/android/repository/platform-tools-latest-windows.zip)
   - [macOS](https://dl.google.com/android/repository/platform-tools-latest-darwin.zip)
   - [Linux](https://dl.google.com/android/repository/platform-tools-latest-linux.zip)

   (These are the download links of Google's
   [SDK Platform-Tools page](https://developer.android.com/tools/releases/platform-tools).)

   The zip holds a single folder named `platform-tools`. Open the zip and
   drag that folder into `GalaxyQuest-converter`. You should end up with
   `GalaxyQuest-converter/platform-tools/adb` (`adb.exe` on Windows). On
   Windows, *Extract All* puts the `platform-tools` folder inside another
   one named `platform-tools-latest-windows`: move it out of there into
   `GalaxyQuest-converter`.

### 3. Open a terminal in that folder

- **Windows:** open the `GalaxyQuest-converter` folder in File Explorer,
  click in the address bar, type `cmd` and press Enter. Then tell this
  window where adb is:

  ```
  set PATH=%PATH%;%CD%\platform-tools
  ```

- **macOS and Linux:** open a terminal, `cd` to the folder, then:

  ```
  export PATH="$PATH:$PWD/platform-tools"
  ```

Check that both tools answer (`py` on Windows, `python3` on macOS and
Linux):

```
python --version
adb devices
```

The first must print Python 3.8 or newer. The second must list one device
with the word `device` next to it. `unauthorized` means the USB debugging
question is waiting in the headset (step 1); an empty list means the cable
carries no data or developer mode is off.

### 4. Install the app

```
adb install --no-incremental -r GalaxyQuest.apk
```

It ends with `Success`. Keep `--no-incremental`: with an incremental
install (the default of recent adb versions) the app does not start.

### 5. Extract your disc with Dolphin

In Dolphin's game list, right-click the game, *Properties*, *Filesystem*
tab, right-click the disc at the top of the list, *Extract Entire Disc...*,
and choose a new, empty folder named `extracted` inside
`GalaxyQuest-converter`. When it is done, `extracted` holds a `DATA` folder
with `sys` and `files` in it.

(Or on the command line:
`DolphinTool extract -i "Super Mario Galaxy.rvz" -o extracted`.)

### 6. Convert the game files

```
python tools/cook/cook.py extracted cooked --with-movies
```

(On Windows: `py tools/cook/cook.py extracted cooked --with-movies`.)

This reads `extracted` and writes the converted game into a new `cooked`
folder (3.3 GB), in a few minutes at most. When it is done it prints
`cooked ... disc files in ...s`, a table of file types and a few lines
starting with `note`: those are normal. The converter also takes a few pieces of data
from the game's program (`sys/main.dol`), which is why it wants the whole
extracted disc.

- Without `--with-movies` the prologue and ending movies are left out
  (2.3 GB less): the game skips them and the story goes on.
- If your extracted disc is somewhere else, give its path instead of
  `extracted`, in quotes if it has spaces:
  `python tools/cook/cook.py "D:\Games\SMG extracted" cooked --with-movies`.

### 7. Copy the game files to the headset

```
python tools/push_data.py cooked
```

(On Windows: `py tools/push_data.py cooked`.)

It packs the `cooked` folder, copies it over USB and unpacks it on the
headset: several minutes, and it needs about 3.3 GB of free space on the
computer meanwhile. It ends with `done: the game files are in ...`. Leave
the headset connected until then.

- `adb not found`: the terminal does not know where adb is. Run the `set
  PATH` (or `export PATH`) line of step 3 again in this window.
- `no headset found`: see the `adb devices` check of step 3.
- Without adb, you can copy the `cooked` folder with the computer's file
  manager instead, the headset connected over USB (for example into
  *Download*), and pick it on the app's setup screen (below).

### 8. Play

Put the headset on and start **GalaxyQuest** from *Library*, *Unknown
Sources* (apps you install yourself are listed there, not in the main
grid). The game starts on a giant screen in front of you; X or the Menu
button opens the pause menu, with the VR settings beside it.

### If something goes wrong

- **`python` is not recognized, or opens the Microsoft Store** (Windows):
  use `py` instead.
- **`adb` is not recognized**: run the `set PATH` line of step 3 in this
  terminal window; it is forgotten when the window closes.
- **The app does not start after installing it**: it was installed without
  `--no-incremental`. Install it again with the command
  of step 4.
- **The app shows a setup screen instead of the game**: it found no game
  files. Run step 7, or pick the folder you copied on that screen (see
  below).
- **A folder shows as *Not converted* or *Convert again*** on the setup
  screen: run step 6 with the current converter, then step 7.
- **A folder shows as *Unknown disc*** on the setup screen: it has none of
  the folders the game keeps its texts in (`EuEnglish`, `UsEnglish`...).
  The copy is incomplete, or the disc is not Super Mario Galaxy: run
  steps 6 and 7 again.

### Where the game files go

The app reads the game from its own storage folder on the headset,
`/sdcard/Android/data/com.galaxy.quest/files/game`, and keeps its saves
in its private storage. No path on your computer is built into it:
`tools/push_data.py` copies the converted files to that folder, from
wherever you converted them.

If the app finds no game files there, it opens a **setup screen** instead
of the game. It lists the folders on the headset that hold the game's
files: aim at one and press A to play from it (the app remembers it). To
list folders outside the app's own storage, such as *Download*, press
*Allow access to all files* and allow it in the settings page that opens;
then come back to the app. A folder of files extracted from the disc but
not converted shows as *Not converted*: convert it with `cook.py` first.
One converted by an older `cook.py` shows as *Convert again*: convert the
disc again with the current one.

- **Updating**: install a newer APK over the old one with the same `adb
  install` command. Your saves and game files stay.
- **Uninstalling** deletes the saves and the game files with the app.
- An APK you built yourself is signed with your own key. To switch between
  it and the released one, uninstall first (back up the saves first, see
  below).

### Backing up and moving your saves

The saves stay in the app's private storage on the headset. To keep a copy
on your computer, connect the headset as for the installation and run,
in the converter's folder (`GalaxyQuest-converter.zip` on the release page;
it needs Python and adb as in the [manual installation](#installing-manually),
also if you installed with the Windows installer):

```
python tools/saves.py backup
```

(On Windows: `py tools/saves.py backup`.)

It writes `GalaxyQuest-saves-<date>.tar` (a few dozen kB). To put it back,
after a reinstall or on another headset with GalaxyQuest installed:

```
python tools/saves.py restore GalaxyQuest-saves-<date>.tar
```

Restoring closes the app and replaces its saves on that headset (it backs
up the ones it replaces first, next to the file). A save belongs to the
disc it was made with: one from the European disc shows up when you play
the European disc, one from the American disc the American one.

## Controls

| Touch Plus | Wii | In the game |
|---|---|---|
| Left thumbstick | Nunchuk stick | Move |
| A | A | Jump, talk, confirm. Hold to float as Boo Mario or skip a cutscene or a dialogue |
| B or Y, or a flick of either controller | Shake | Spin |
| Right trigger | B | Shoot star bits, cancel |
| Right controller aim | Pointer | Collect star bits, grab Pull Stars, point at menus |
| Left trigger | Z | Crouch, ground pound, long and back flip jumps |
| Left grip | C | Put the game camera behind Mario |
| X or Menu | − and + | Pause menu (with the VR settings) |
| Right stick left / right | D-pad | Turn the view round Mario: the diorama, or on the giant screen the game camera (*Invert camera* in the VR settings swaps the two sides) |
| Right stick up | D-pad up | First-person look |

To recentre the view, hold the Meta button on the right controller. All the
details, and the settings file, are in [docs/CONTROLS.md](docs/CONTROLS.md).

## Building from source

The release APK is built from this repository as it is; you can build it
yourself too. You need:

- the [Android NDK r29](https://developer.android.com/ndk/downloads),
- the Android SDK with *build-tools* and the *android-36* platform (from
  Android Studio's SDK Manager, or `sdkmanager`),
- a JDK 17 or newer (Android Studio's own works),
- [CMake](https://cmake.org/download/) 3.24 or newer, [Ninja](https://ninja-build.org/),
  Python 3 and bash (on Windows, [Git Bash](https://git-scm.com/downloads)).

```
git clone https://github.com/bigmak94/GalaxyQuest.git
cd GalaxyQuest
export ANDROID_NDK_HOME=/path/to/android-ndk-r29   # if not found by itself
export ANDROID_HOME=/path/to/Android/Sdk           # likewise
./build_android.sh
tools/package_apk.sh
adb install --no-incremental -r out/GalaxyQuest.apk
```

`python tools/package_converter.py` makes the release's other download,
`out/GalaxyQuest-converter.zip`: the converter and `push_data.py` with the
modules they import.

The first build downloads the Khronos OpenXR loader from Maven Central.
`tools/env.sh` lists every variable the scripts read (`JAVA_HOME`, `CMAKE`,
`NINJA`, `PYTHON`, `ADB`). The builds are made on Windows 11 with Git Bash;
Linux and macOS use the same scripts but are untested.

## How it works

- `decomp/` holds the [Petari](https://github.com/SMGCommunity/Petari)
  sources with the changes the port needs: little-endian and 64-bit fixes
  and the hooks of the VR presentation, all marked `TARGET_PC`.
  `git diff petari-base -- decomp` shows them against the original. Left
  out of this repository: the few pieces of game data Petari keeps from
  the game's executable (the error screens' archive and two tables), which
  the converter takes from your own disc instead.
- `platform/` replaces the Wii: memory laid out as on the console, threads,
  the disc and saves, a graphics processor that turns the game's GX
  commands into OpenGL ES, the DSP that mixes the sound, controllers, and
  the OpenXR app with the VR presentation (`platform/src/xr/`).
- `tools/cook/` converts the game's files to the layout the port reads.

[docs/TECHNICAL.md](docs/TECHNICAL.md) goes through it all in detail, with
the development tools (the headless test runner and its switches).

## Status

The game plays from the prologue on, in the diorama and on the giant
screen, and all 44 galaxies load and play (checked with an automated tour
of them). Known gaps:

- Miis are not available (there is no console Mii database): you pick an
  icon for a save file instead.
- The HOME menu is not implemented; the Meta button takes its place.
- The sun's lens flare doesn't show (it reads the picture back, which the
  port's renderer can't).
- The Japanese and Korean discs (which would run in their own language)
  have not been tested.

Bug reports are welcome in the
[issues](https://github.com/bigmak94/GalaxyQuest/issues), ideally with
the log `tools/app_log.sh` prints after a session.

## Thanks

This port stands entirely on the work of the
**[Petari](https://github.com/SMGCommunity/Petari) team** and the
**SMGCommunity**, who spent years decompiling Super Mario Galaxy back into
readable source code and gave it to everyone under CC0. Without their
patient work none of this would exist: thank you!

Thanks as well to:

- the [Dolphin](https://dolphin-emu.org/) team, whose documentation of the
  Wii's graphics and audio hardware guided the platform layer, and whose
  tools extract the disc;
- AMD for [FidelityFX CAS](https://github.com/GPUOpen-Effects/FidelityFX-CAS),
  the Inter Project for the [Inter](https://github.com/rsms/inter) typeface
  of the VR panels, and the Khronos Group for the OpenXR loader (their
  licenses are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md));
- Nintendo, for Super Mario Galaxy.

Super Mario Galaxy, Mario and their logos are trademarks of Nintendo.
GalaxyQuest is an unofficial fan project, not affiliated with or
endorsed by Nintendo, and it includes no Nintendo game data.

## License

GalaxyQuest is open source and free for everyone: its code, tools and
documentation are released into the public domain under
[The Unlicense](LICENSE). Copy them, change them, use them, share them or
sell them as you please, for any purpose, without asking anyone.

The decompilation in `decomp/` is the Petari team's work, dedicated to the
public domain under CC0 1.0 ([decomp/LICENSE-Petari.txt](decomp/LICENSE-Petari.txt));
the port's changes to it are under the Unlicense like the rest. The few
third-party parts keep their own licenses: see
[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
