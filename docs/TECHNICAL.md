# How the port works

Technical notes for people working on the port. For playing, see the
[README](../README.md) and [CONTROLS.md](CONTROLS.md).

## Presentation in the headset

- Gameplay is shown as a **diorama**. Mario stands on a tabletop-sized world
  about 1.5 m in front of you and 0.8 m below eye level, at 1/500 scale.
  You look around it and lean in with your own head, much like Max Mustard or
  Astro Bot. The camera never becomes first person, and the game camera's
  pitch and roll never move your view.
- The world follows Mario smoothly, with a small dead zone. Its "up" is
  against Mario's gravity, so he always stands upright. Its facing stays
  where it is (the game camera swinging round Mario turned the whole world
  around the player): the right stick turns it in 45 degree steps behind a
  short blink, and a new area starts from the game camera's facing. A
  sudden change of gravity (a switch, a room's wall becoming the floor)
  also happens behind a blink. The stick follows the diorama rather than
  the game camera's screen: pushing it forward always moves Mario away from
  you, even where the game camera turns upside down on small planets.
  Ordinary jumps don't move the world; it follows once Mario is 0.7 m above
  where he left the ground.
- A galaxy's opening shots and Mario's flight into it play on the virtual
  screen, like cutscenes (in the diorama they flew the world around you).
- The giant screen (a switch on the VR settings panel, `giant_screen`)
  plays the whole game on a 16:9 virtual screen from the game's own camera
  instead of the diorama (the default at first start): 5.33 m wide,
  `screen_distance` away (4.5 m by default; a slider on the settings
  panel's Screen tab). The game draws its 16:9 picture
  squeezed into its 640x456 frame (the
  TV stretched it back out), so the screen's and the HUD panel's targets
  are 16:9 (2048x1152 and 1600x900). The screen's layer is mipmapped and
  asks the compositor for supersampling, since a distant screen shows
  fewer display pixels than it has texels.
- Stereoscopic 3D on the giant screen (`stereo_screen`, a switch on the
  settings panel): frames with a 3D camera are replayed twice into two
  screen targets, one for each eye, and go out as two quad layers with
  `XR_EYE_VISIBILITY_LEFT` and `_RIGHT` (both are published together once
  the right one is drawn, so the eyes never show different game frames).
  The Quest's compositor shows the two as one stereo quad with a swapchain
  for each eye. The two targets are `stereo_resolution` (0.8) times the
  single picture's size, 1638x922, drawn into the lower left part of the
  2048x1152 layer images and shown through the layers' image rectangles, so
  the compositor does the only scaling. Measured in the headset (Good Egg,
  app GPU time a frame): one picture 6.3 to 7.0 ms in play and 8.0 ms in the
  galaxy's opening shots; two at full size 10.6 and 13.2 ms (57 frames a
  second in the opening); two at 0.8 8.6 to 9.0 and 9.7 ms, 60 frames a
  second throughout.
  The replay keeps the game's camera, projection and viewports; the vertex
  shader shifts the 3D draws sideways in clip space by
  `a * min(C - w, m * w)`, with `w` the depth in front of the camera, which
  is the picture from a camera moved sideways with its frustum sheared to
  meet the other one's at depth `C`, the convergence. In distances between
  the player's eyes (the distance between the two eye poses the runtime
  reports), the two pictures then draw a point
  `stereo_far - stereo_depth * d / w` apart, `d` being Mario's depth:
  the farthest things `stereo_far` (0.95) behind the screen, the most the
  eyes can take, and Mario `stereo_depth` (1.75, "3D depth" on the settings
  panel) in front of that. So `a` is 0.95 eye distances and `C` is
  `d * stereo_depth / stereo_far`, following the camera with a 0.4 s
  half-life and jumping on cuts. A screen 4.5 m away leaves under a degree
  between itself and infinity, so a scene kept wholly behind it (the first
  version: 0.8 behind, Mario 0.52 before that) had hardly any depth; now
  Mario stands two metres in front of the screen and the foreground
  comes further out. Nothing is drawn more than 2.5 eye distances apart in
  front of the screen (`m`), 1.3 m from the player. The draws between the
  HUD markers are shifted as a whole to float in front of the scene they
  cover (`2 * stereo_depth - stereo_far` eye distances, at most the 2.5:
  1.3 m away), and widened by the shift so a fade still covers the picture;
  their scissor boxes move with them. The pointer's cursor (the draws
  between the pointer markers, inside the HUD's) is the exception while it
  points into the scene: floating with the HUD it stopped short of what it
  pointed at, and the eyes on the target saw it double. It gets the shift of
  the point under it instead, whose depth the game reports each frame
  (`port_vr_pointer_depth`: its own ray from the camera through the cursor
  against the map's collision, the far plane where it hits nothing), so it
  lies on the surface it points at. Only the map counts: over an enemy or
  a character it lies on the ground behind them.
  Skies are drawn at the far limit whatever their
  model's size. Other orthographic draws (post effects) are not shifted,
  screen-space texgens (water, heat haze) follow the
  shifted position, and each picture keeps its own EFB copies, as the
  diorama's eyes do.
- The app's space (screen, diorama, panels, controllers) is the runtime's
  LOCAL space moved to the head and turned to where it faces (about the
  vertical only) on the first tracked frame of each session, at launch and
  when the headset is put back on, and again when the player recentres
  (`XrEventDataReferenceSpaceChangePending` for LOCAL) or the head's pose
  jumps within a session's first five seconds (tracking settling after a
  wake-up). LOCAL alone can be stale when the game starts: launched right
  after the headset woke up, its origin was 2.15 m from the head, and the
  screen came up beside or behind the player.
- The HUD (coins, star bits, life meter, menus) sits on a transparent panel
  1 m in front of you.
- Menus, the title and file select, and cutscenes appear on a large virtual
  screen. Changes between the two presentations fade through black.
- The right Touch Plus controller is the Wii Remote pointer. In gameplay you
  aim it into the diorama to collect star bits, and the star bits you shoot
  leave from it. On menus it points at the HUD panel or the virtual screen.
- The headset refreshes at 120 Hz and the game runs at 60 Hz. With Meta's
  Application SpaceWarp the game's frames go to the headset with motion
  vectors, and the headset synthesizes the refresh in between: the world
  gliding past as the diorama follows Mario no longer shows each frame
  twice (a doubled, smeared look on grass and flowers). Without it (the
  `space_warp` setting) each game frame stays up for exactly two
  refreshes. The render resolution adapts to the GPU load (dynamic
  resolution), from 0.8 to 1.6 times the headset's recommended eye size.

## Status in detail

Working (played in the headset, and checked on it through the headless
runner described below):

- boot, title, file creation, prologue and gameplay; the save file is kept
  on the headset
- all 44 galaxies load and play (`tools/galaxy_tour.sh`), and 1,000 s of
  self-play in the observatory (`PETARI_WANDER`) runs without a crash and
  with memory flat
- the GX graphics pipeline, including TEV, Z textures and EFB copies, in
  GLES 3.2 with batched draws
- audio: the DSP mixer and streamed music, played through AAudio
- the prologue and ending movies (THP), with sound
- Wii Remote and Nunchuk emulation driven by Touch Plus, including tilt for
  the Star Ball and Ray surfing
- the diorama rig, HUD panel, virtual screen, giant screen, and culling
  against the headset's view

Known gaps:

- GPU time per eye: in the headset the old fixed 1428x1496 eye took
  4.3-5.5 ms in Gateway Galaxy (GPU at 456-640 MHz). At the GPU's lowest
  clock (285 MHz, headless) an eye takes 7.5 ms at 1428x1496, 9.5 ms at
  1680x1760 and 13.2 ms at 2184x2288; fixed foveation
  (`GL_QCOM_texture_foveated`) saves nothing measurable with this
  renderer. At 120 Hz each eye has one refresh (8.3 ms, including the
  compositor's 1-2.3 ms), which is what the dynamic resolution keeps to.
  In the headset, lying unworn on a desk (compositor 2.3 ms), Gateway
  Galaxy settles at 1.0-1.15 with the game at 59.5-60 fps and 0-7 late
  frames a second.
- Miis are not available (the console Mii database doesn't exist here). You
  pick an icon instead.
- The HOME menu is not implemented. The Meta button takes its place.
- The renderer cannot read the frame back to the game (`GXPeekARGB` and
  `GXPeekZ`). The sun's lens flare, which samples the frame, never shows.
  What the pointer is on is found by casting its ray against the level's
  collision instead.

## How it works

| Piece | Where | Notes |
|---|---|---|
| Game code | `decomp/` | Petari sources (CC0) with little-endian and 64-bit fixes and VR hooks, guarded by `TARGET_PC` / `__MWERKS__`; `git diff petari-base -- decomp` lists them |
| Memory | `platform/src/os/os_mem.cpp` | MEM1/MEM2 mapped at 0x80000000/0x90000000 in a reserved low 4 GB window; the game library loads at 0x98000000, so 32-bit pointers in data files stay valid |
| Data | `tools/cook/` | Offline conversion of RARC, J3D, KCL, BCSV, layouts, fonts, messages, particles and JAudio formats to little-endian. The few pieces of data the game's executable holds (the error screens' archive, the StoryEvent and GalaxyID tables) come from the player's `sys/main.dol` too (`dol_data.py`), loaded at boot by `platform/src/dvd/dol_data.cpp` |
| OS / SDK | `platform/src/{os,dvd,nand,input,sdk}` | Threads, alarms, interrupts, DVD, NAND saves, WPAD/KPAD, stubs |
| Graphics | `platform/src/gx/` | The GX FIFO is recorded per frame (`gx_recorder.cpp`) and replayed with generated GLSL (`gl_shadergen.cpp`, `gl_renderer.cpp`). Display lists are decoded once and reused while they and their vertex data are unchanged. Draws are batched through storage buffers. A worker thread prepares frames, and a compile thread plus an on-disk binary cache avoid shader stalls |
| Audio | `platform/src/audio/` | High-level emulation of the DSP mixer (AFC ADPCM, PCM, resampling, filters, volume ramps, FX delay lines). It renders one 80-sample sub-frame each time the game has updated the voices, as the console's DSP does: streamed music relies on following its voices that closely to loop. The game's audio blocks go into a ring that AAudio's callback drains at 48 kHz; the emulated audio interface starts a new block whenever about 32 ms remain queued, so the headset's audio clock paces the game's audio |
| Movies | `platform/src/sdk/thp_video.cpp` | Portable THP decoder (the SDK's is Broadway assembly). It writes Y/U/V straight into GX I8 textures, which the game's own TEV setup converts to RGB. 640x368 frames take about 1.7 ms on the Quest CPU. `tools/thp_test/` checks it on the PC |
| VR | `platform/src/xr/` | OpenXR app (`xr_app.cpp`), diorama rig (`vr_rig.cpp`), presentation (`vr_game.cpp`) |

The game records its camera, Mario's position and hints (whether the
diorama is allowed, and whether the pointer is on a menu) into the GX stream
from `GameScene::draw3D`. It also brackets `draw2D` with HUD markers, and
`GameSystem::draw` brackets what it draws over the scene the same way (the
save and error windows, the pointer's cursor, the system wipe: drawn into
the eyes' images instead, the save window covered the whole view out of
the pointer's reach). The renderer draws the perspective 3D scene through
each eye's VR matrices and sends the HUD draws to a separate panel.

In the diorama:

- The diorama holds Mario at its anchor, not the point the game camera
  watches: that point leads, trails or frames things for a camera 10-20 m
  away, while the VR eye sits a fixed distance from the anchor. Around the
  Dino Piranha's planet (Good Egg Galaxy, 840 units in radius) the
  watched point trailed Mario by up to 1000 units, through the planet,
  and the eye was inside the planet in 35% of a headless fight
  (`PETARI_CAMLOG`). The game says when to follow the watched point
  instead (`PORT_GX_CAMERA_CENTRE_PLAYER` off): a galaxy's opening shots,
  and event cameras watching a point over 2500 units from Mario. The game
  camera's own jump damping is replaced by the rig's: the pivot stays at
  the height Mario left the ground from (`PORT_GX_CAMERA_GROUNDED`) until
  he is 350 units above it. The world's up is smoothed less while it turns
  steadily (Mario running round a small planet), so it trails his gravity
  by at most about 12 degrees instead of 30-55, which had put the eye
  below his horizon.
- The game's letterbox bars (`CinemaFrame`, shown through a galaxy's whole
  opening) are left out of the diorama; the frame closing to black and
  opening from it becomes a fade of the whole view (`port_vr_wipe`).
- A comet mission's screen filter (`GalaxyCometScreenFilter`, a tint over
  the whole TV picture, darkest in the middle of its top) is left out of
  the diorama too: on the HUD panel it was a black patch in the middle of
  the view. On the virtual screen it is drawn as on a TV.
- On the giant screen no laser is drawn from the controller (the game's
  cursor is on the screen); it shows only while the ray is on one of the VR
  layer's own panels (`vr::setAimLength`) or the setup screen is up.
- When level geometry hides Mario (a collision ray from the headset to him
  is blocked), the geometry between your eyes and him is dithered away: a
  cone from each eye to Mario, plus a small sphere around the eye
  (`vr::setCutaway`). Shaders have a cutaway variant that is used only then,
  because its `discard` costs the GPU its early depth rejection (10-20% more
  GPU time while it is on).
- Star pointer targets, such as star bits, Pull Stars and enemies, are hit
  against the controller's aim ray in the game world
  (`port_vr_pointer_ray`), not the game camera's 2D cursor. The ray ends on
  the first map surface it meets, or as far past Mario as the original aims
  star bits past its camera (`MR::calcVrPointerAimEnd`); the laser is drawn
  that long (`port_vr_pointer_reach`). Shot star bits leave from the
  controller instead of from beside the game camera, which in the diorama
  is behind the player's head, and fly to the laser's end.
- The game draws its models through display lists, most of them strips of
  a few vertices (Good Egg Galaxy: about 18,000 draws in 500 list calls a
  frame). Decoding their vertices was most of the game thread's time. The
  recorder keeps each list's decoded vertices (`gx_recorder.cpp`, display
  list cache) and reuses them while the list's bytes, the vertex format
  state and the vertex array data it read are the same. The array data is
  checked with a hash, once per FIFO flush, so models the CPU deforms are
  decoded again. A list of draws alone is replayed without being parsed.
  The worker adds a draw that follows one with the same state to its batch
  without working the state out again. In Good Egg Galaxy (headless) the
  game thread went from 6-8 ms to about 4 ms a frame and the worker from
  about 5 ms to 2 ms; a frame is about 200 batches. `PETARI_DLCHECK=1`
  decodes every cached draw again and compares.
- Frame pacing (`renderFrame` in `xr_app.cpp`): the display runs at 120 Hz
  and the game's video retrace comes from the frame loop every second
  refresh (`port_vi_retrace`), so each 60 Hz game frame is shown for
  exactly two refreshes. The left eye of a game frame is rendered on the
  first refresh of a pair (its swapchain image stays acquired), the right
  eye on the second, and both images are released together; the set is
  submitted from the next refresh on, for two refreshes, while the other
  of two swapchain sets is rendered. Each refresh carries one eye of GPU
  work: the runtime holds the frame loop back when a refresh's work
  overruns it. And the compositor only ever gets a set whose two eyes are
  finished and show the same game frame: submitting each eye as it was
  rendered let late frames show the two eyes of different game frames.
  The game hands each frame to the renderer's worker as it is presented,
  and the per-frame buffers rotate between three sets
  (`Renderer::Impl::upload`), so neither preparation nor uploads wait for
  the GPU. At other refresh rates (thermal throttling drops to 72 Hz) both
  eyes are rendered every refresh and the game keeps a free-running
  59.94 Hz clock.
- Application SpaceWarp (`XR_FB_space_warp`, the `space_warp` setting, on
  by default at 120 Hz): the runtime runs the frame loop at 60 Hz; each
  frame renders both eyes plus, per eye, motion vectors (`GL_RGBA16F`) and
  depth (`GL_DEPTH24_STENCIL8`) at the size the runtime recommends, and the
  compositor synthesizes every other refresh from them. With it the doubled
  image goes away: at 120 Hz a frame shown on two refreshes of a
  low-persistence display is seen twice in the same place while the eye
  follows the world moving past, so everything the diorama scrolls looked
  smeared. Motion vectors are this frame's normalized device coordinates
  minus the last frame's for the point seen at each pixel, the head's
  motion included (as in Meta's samples). They are worked out from the
  scene's depth (`vr::renderMotion`): the game marks where its 3D scene is
  complete (`PORT_GX_MARK_SCENE_DEPTH`, before the image effects and the
  Z clear), and there the renderer copies the eye's depth and stencil at
  the motion vector size. A point is taken to stay put in the world while
  the rig and the head move; Mario's draws (between
  `PORT_GX_MARK_PLAYER_*`, in `MarioActor::draw` and the player decoration
  buffers) leave 1 in the stencil buffer, and those pixels move with his
  centre instead. The HUD panel and the virtual screen stay put in the
  room. Enemies and other objects that move on their own still move at 60
  frames a second (their pixels get the motion of the world around them).
  Frames after a rig jump, a change between the diorama and the virtual
  screen, or a warp of Mario are marked not to be extrapolated. The eyes
  always go to the same pair of swapchains: the compositor keeps its
  SpaceWarp state per eye swapchain, and alternating between two sets (as
  the paired refreshes do) made it start over every frame and synthesize
  nothing (VrApi `ASW=0`; `AppMVSource ... InitEyeTexDependentResource` in
  logcat every frame). With it working, VrApi shows `ASW=120, Type=App`.
  It does not save GPU time here: the game makes 60 frames a second and
  each was already rendered once (shown on two refreshes); the compositor's
  synthesis adds about 0.3-0.5 ms a refresh.
  `appSpaceDeltaPose` is the rig's motion (the room's pose in the world
  relative to the last frame's). Depth written for the far background
  stops just short of the far plane, so the compositor keeps the motion
  vectors given there.
- Dynamic resolution (`vr_game.cpp`): each eye renders into a target of
  the current scale, between 0.8 and the `resolution` setting (1.6 times
  the recommended size); the composite resamples it into swapchains of a
  fixed size (the setting, at most 1.25 times the recommended size, about
  the display's own density in the middle). Targets exactly the size
  rendered matter on this tiled GPU: rendering part of a larger target
  still loads and stores the whole of it in every render pass. The scale
  steps down when the frame loop misses refreshes in the diorama, or when
  GPU timer queries on the eyes come close to the refresh, and back up
  after 1.5 s of headroom (not for 20 s to a scale that missed
  refreshes). A missed refresh counts only when the frame loop's own work
  was not late (it took under three quarters of the refresh) and the
  session has focus: in a play session the GPU needed 2.6-3.6 ms of the
  8.3 ms per eye, yet refreshes the CPU missed held the scale at 0.8-1.05.
  The GL timer undercounts on this tiler: VrApi puts the app at 10-14 ms
  of GPU per 60 Hz frame (both eyes) at scale 0.8-0.9 in the castle
  garden, the GPU 90-97% busy at its top clock (640 MHz), so the scale
  stays there. Most of an eye's cost does not depend on its size (the
  game's draws and EFB copies: headless, an eye takes about 9 ms at
  0.8x and 1.0x, 12 ms at 1.25x); fixed foveation
  (`GL_QCOM_texture_foveated` on the eye targets) saves nothing measurable.
- With Super Resolution (the `super_resolution` setting, on by default)
  the diorama goes to the compositor at its render size, as the lower left
  part of the swapchain image (`imageRect`), with
  `XR_FB_composition_layer_settings`' quality sharpening (Meta Quest Super
  Resolution) on the layer: the compositor scales it to the display once,
  instead of after a bilinear pass in the app. The virtual screen still
  fills the whole image.
- Passthrough around the giant screen (`passthrough`, off by default):
  Meta's `XR_FB_passthrough` (the manifest declares
  `com.oculus.feature.PASSTHROUGH`, without which the runtime does not list
  the extension). The feature and one reconstruction layer are made the
  first time the setting asks for them, and paused while it does not. While
  they run, the frame's first layer is the passthrough layer, and the eye
  layer goes out with `XR_COMPOSITION_LAYER_BLEND_TEXTURE_SOURCE_ALPHA_BIT`:
  around the screen the eye images are cleared to transparent black instead
  of the dark (premultiplied alpha; the laser and the skip ring blend into
  them as before), so the room shows there. The clear's alpha fades over
  0.3 s when the setting changes. The diorama's eye images are opaque. In
  the headless simulator a flat grey-green stands for the room. Measured
  in the headset (unworn, Good Egg on the giant screen, SpaceWarp on): the
  compositor's GPU time goes from 1.9 ms a refresh to 3.1-4.2 ms and the
  GPU from 65% to 82% busy; the game still shows 592-599 of its 600 frames
  in 10 s (597-600 without), with 6-22 refreshes missed instead of 0-6.
- The HUD panel (with the pause menu and dialogs) and the VR settings panel
  go to the compositor as quad layers of their own (`XrCompositionLayerQuad`,
  premultiplied, sRGB; `vr::uiLayer`), as Meta recommends for text: sampled
  once, at full sharpness whatever the eye images' render size. With Super
  Resolution they had been drawn into the eye image at render size and
  lost about a third of their pixels. The HUD's layer only goes out while
  the game draws something into it (a layer costs the compositor its area
  on every refresh), and the settings panel draws the pointer's reticle into
  its own image (the laser, in the eye layer, is under it).
  `PETARI_XRSIM_LAYERS=1` does the same in the headless simulator.
- The screen's 3D pictures (the giant screen's gameplay) have a render
  scale of their own, moved by the same rules as the eyes' (and by the
  runtime's counters only): from 1 (2048x1152) down to three quarters of
  `min_resolution`. A smaller picture is drawn into a target of exactly
  its size and goes into the lower left part of the screen layer's image,
  shown through the layer's image rectangle, as the stereo pair's pictures
  are (each `stereo_resolution` times the scaled size). Frames without a
  3D camera (menus, movies) stay at the full size. Each of the two scales
  is judged afresh when the presentation changes.
  `PETARI_FIXED_SCALE` holds whichever is in use.
- Meta Quest Super Resolution's sharpening is asked for only while the eye
  layer holds the diorama: around the screen that layer is dark or
  see-through.
- The dynamic resolution reads Meta's performance counters
  (`XR_META_performance_metrics`: the app's and the compositor's GPU time,
  the GPU's utilization) when the runtime has them, and judges the eyes by
  them instead of GL timer queries, which miss the tiler's resolves (the
  user's session: timer 3.3-3.9 ms an eye at scale 0.8-0.95 while refreshes
  were missed). An eye's budget is the refresh minus the compositor's GPU
  time; the scale goes down past 92% of it and up after 1.5 s under 72%,
  not while the GPU is over 95% busy. The counters are logged every 10 s
  (`vr: runtime counters`). `min_resolution` (0.8) is the floor; headless
  (`PETARI_FIXED_SCALE`, Good Egg start), a frame costs 17.4 ms of GPU at
  0.8, 23.2 at 1.0, 27.0 at 1.1 and 32.5 at 1.25.
- The `sharpening` setting (the panel's FidelityFX CAS switch) composites
  the diorama through AMD FidelityFX CAS (the algorithm of `ffx_cas.h`,
  MIT): a 3x3 contrast-adaptive sharpen when the diorama and the eye image
  have the same size, CAS's 12-tap scaling filter otherwise.
- The app asks for Meta's SustainedHigh CPU and GPU level range
  (`XR_EXT_performance_settings`, the `high_clocks` setting). Without it
  the system ran the CPU at level 2 (1.38 GHz) in gameplay. It also queries
  Meta's recommended eye size each frame (`XR_META_recommended_layer_resolution`,
  Meta's dynamic resolution for native apps; logged as `vr: runtime
  recommends ...`), which the runtime requires before it grants GPU level 5;
  the clock was already at the GPU's top, 640 MHz, in gameplay. The
  recommendation itself (the swapchain's maximum while the GPU was 95%
  busy) is not followed.
- Characters are lit as seen from the headset: the game's actor lights are
  mostly "FollowCamera" lights, placed in view space, and the rim light
  (`GX_LIGHT2`, alpha channel) sits on the camera. Lit from the game
  camera, a face seen from the front in the diorama took the rim across it
  and looked white. `LightFunction` places those lights relative to the
  headset while the diorama is shown (`port_vr_cull_view`), and the vertex
  shader moves any remaining light at the view space origin to the eye.
- Choosing a galaxy in an observatory dome, and the first-person view, are
  shown on the virtual screen, where the pointer lands exactly where you aim.
- So are launch and sling star flights (from the launch until the star lets
  go of Mario) and trips through pipes: the objects report themselves with
  `port_vr_transit_begin`. The game camera frames those on its own terms. A
  flight crosses space faster than the diorama follows, while the world
  turned with the gravity of each planet on the way, and for a pipe the
  camera pulls back to show the whole planet, which put the viewer inside
  it.
- Cannons (`MarioLauncher`) report themselves the same way, from the moment
  the sight appears until Mario lands or climbs back out. The shot goes
  along the game camera's ray through the cursor, and that camera sits in
  the cannon's mouth: in the diorama the player saw the cannon from outside
  with the sight on the HUD panel, and could not tell where it aimed.
- Screen wipes (fades, and the ring that closes on Mario) cover the whole
  view instead of the HUD panel.
- Water and heat haze sample a capture of the screen where each surface
  lands on it. The renderer recognises those texture coordinates (they
  match the game camera's projection) and uses the eye's screen position
  instead, since in VR the capture holds that eye's view. Each eye keeps
  its own EFB copies, keyed by destination address like texture memory,
  so effects that read the previous frame's capture (the crystals Toads
  are trapped in) see that eye's last view.
- Skies are modelled around the game camera, which in the diorama is
  metres from your eyes; the game marks their draws and the renderer draws
  them around the eye, at the far plane.
- The game pauses whenever the headset session loses input focus (headset
  off, or the system menu open), and returning opens its pause menu.
- Holding A skips cutscenes (`platform/src/port/cutscene_skip.cpp`).
  `GameScene::update` reports which kind is running. Movies, the galaxy
  intro camera and the fly-in take the request through their own skip
  paths. Other cutscenes (DemoDirector demos) have no general way to end
  early, so the game logic runs fast-forward, undrawn and muted, with A
  pressed for text boxes: held for two updates, released for one.
  Cutscene dialogue (`TalkStateEvent`) turns a page only while A is held on
  from the update before, so the earlier press on alternate updates never
  got through a talk: the fast-forward gave up after 10,800 updates (about
  8 s of a dark view ignoring the buttons) and the talk went on as before.
  A yes/no choice stops it (`YesNoController`). The VR layer draws the hold
  ring and dims the view while this runs. A scene change stops it too
  (`GameSystemSceneController::isChangingScene`, `port_skip_scene_change`):
  fast-forwarded through Mario's jump out of a dome into the star select,
  the game stopped for good. The next part of a scene is skipped on only
  while A has been held since the skip without a break; a new press (the
  one confirming a galaxy right after a lecture was skipped) is the
  player's own.
- The setup screen (`vr_setup.cpp`): without converted game files in the
  folder chosen before (`game_path`) or in the app's own `files/game`, the
  app does not boot the game but shows a panel listing the folders on the
  headset that hold them. A thread searches the app's own storage folder
  and, with Android's all files access (`MANAGE_EXTERNAL_STORAGE`, asked
  for through JNI in `xr_app.cpp`), the shared storage four levels deep.
  A folder counts when it has `sys/fst.bin` and `files/`, and is converted
  when `files/ObjectData/Coin.arc` starts `CRAR` (the disc's own archives
  are Yaz0). Picking one saves `game_path` and boots the game from it.
- The disc's region (`port_dvd_identify` in `dvd.cpp`): each region's disc
  keeps its texts and translated layouts in language folders of its own
  (`EuEnglish`, `UsEnglish`, `JpJapanese`, `KrKorean`...), and the game
  picks the folder from the disc's game code and the console's language
  (`Language.cpp`, whose table the port indexes by the code in low memory
  instead of the Korean build's fixed row). The port reads the region off
  those folders in the disc's file table (`sys/fst.bin`, which every
  conversion has and every file lookup goes through), puts the matching
  code (`RMGP01`, `RMGE01`...) at 0x80000000 and answers `SCGetLanguage`
  with a language that disc has: the one of the `language` setting when the
  disc has its texts (the European disc: English, French, German, Spanish,
  Italian; the American one: English, French, Spanish), otherwise the
  disc's first. The game reads it once, when `GameSystemObjHolder` is made,
  so a change on the settings panel shows at the next start. (The European
  disc's `EuDutch` folder holds the English texts again: not offered.) With
  a wrong code the game asks for another region's folder and stops at its
  first text archive (`FileRipper`: "File isn't exist").
  The European and American discs' other files are the same but for a few
  object placements (Gusty Garden, Rolling Gizmo) and the wording of the
  texts. A folder whose file table names none of those text folders, or
  whose copy lacks the texts, shows as "Unknown disc" on the setup screen.
- Every save file can be played with Mario or Luigi from the start
  (`FileSelector::isUserFileAppearLuigi`): the Mario/Luigi switch the game
  shows once Mario has finished it is on every file's start screen.
- The camera's turns (`invert_camera`, on by default): the game moves its
  camera round Mario the way the D-pad is pressed, so the view turns the
  other way. With the setting, `CameraLocalUtil`'s two tests of the D-pad
  for the camera swap sides (so do the two arrows of the camera guide,
  `CameraInfo`), and the diorama's snap turn takes the other sign: pushing
  the right stick right turns the view to the right. Pages and menus read
  the D-pad themselves and keep their sides.
- The settings (`petari_vr.ini`): one table in `vr_game.cpp`
  (`vr::Setting`: key, range, default, how to read and change it) serves
  the file's loader and the settings panel (`vr_settings.cpp`), whose four
  tabs are tables of rows over those keys (a switch, a stepper or a
  slider). The panel writes only the lines of the settings changed on it.

## Development tools

`tools/run_headless.sh <seconds> [--no-push]` pushes the build and boots it
from an adb shell, without VR. It saves PNG captures to
`/data/local/tmp/petari/shots` and symbolises crashes. Behaviour is
controlled with environment variables:

| Variable | Effect |
|---|---|
| `PETARI_INPUT` | Scripted controller input, e.g. `"28-28.4:A\|B,30-36:PX=-0.25\|PY=0.27,33:A"`. Items are `A B 1 2 PLUS MINUS HOME Z C UP DOWN LEFT RIGHT SPIN SX= SY= PX= PY=` |
| `PETARI_SHOT_MS`, `PETARI_SHOT_FROM=s` | Capture interval (default 2000); first capture at s seconds (for bursts of close captures) |
| `PETARI_VRTEST`, `PETARI_VRHEAD="x,y,z,yaw,pitch"`, `PETARI_VRSIZE=WxH[,WxH...]`, `PETARI_FOVEATE=gain[,gain...]` | Also render the frame through the VR rig; time an eye at each size (and with fixed foveation at each gain, 0 = none) |
| `PETARI_GLSTEPS=a,b,...`, `PETARI_GLITEMS=n`, `PETARI_DUMP=n`, `PETARI_COPYDUMP=dir`, `PETARI_COPYDUMP_EYE=1` | Partial renders (also of the VR test view), batch list of every nth prepared frame (1: all; markers, depth state and the player tag per batch), register dump with the first n textures (default 16), EFB copies as PNGs (of the left eye with `PETARI_COPYDUMP_EYE`) |
| `PETARI_STAGE="Galaxy[:scenario]"` | Enter that galaxy two seconds into ordinary gameplay (e.g. `HeavensDoorGalaxy:1`); `tools/galaxy_tour.sh` runs a list of galaxies and collects captures and crash reports in `out/tour/` |
| `PETARI_MOVIE=n` | Play movie n (0 = PrologueA .. 6 = EndingB) two seconds into gameplay in a stage with a movie player (the castle garden or the observatory) |
| `PETARI_NERVES=N`, `PETARI_THREADS=1` | Trace N state-machine transitions; dump emulated threads at exit |
| `PETARI_WANDER=s` | From s seconds on, play by itself (pseudo-random stick, jumps, spins, crouches) for soak tests. The runner logs its memory use every 30 s |
| `PETARI_XRSIM=1`, `PETARI_XRHEAD="yaw,pitch"` | Run the headset presentation (`vr_game.cpp`) with two simulated eyes and save both swapchain images side by side (`frame_NNN_xr.png`) |
| `PETARI_XRSIM_MV=1` | With `PETARI_XRSIM`, render SpaceWarp's motion vectors and depth too and save the left eye's as `frame_NNN_xr_mv.png` (red/green: horizontal/vertical motion around grey, 1/40 of the view per frame saturates; blue: 0 world, 128 fixed in the room, 255 Mario), with their average per kind of pixel in the log |
| `PETARI_VRLIGHT_OFF=1` | Light the characters from the game camera in VR as the console did (no headset-relative lights; for A/B captures) |
| `PETARI_XRSIM_FPS=72`, `PETARI_PERFLOG=1` | Keep rendering the simulated headset view at that rate after the first capture; log game and renderer frame times every 10 s (the app logs them in the headset too whenever the game drops below 58 fps) |
| `PETARI_CUTTEST=1` | Keep the VR cutaway on and three times as wide, so it shows in captures |
| `PETARI_WAV=path`, `PETARI_AUDIOLOG=1` | Record the game's audio; log audio pacing every 10 s (otherwise only late blocks and underruns are logged, in the headset too) |
| `PETARI_SELOG=1`, `PETARI_DSPLOG=1` | Log each sound effect's start and end (and those still running long after their stop); list the DSP voices playing once a second |
| `PETARI_SETEST="t0-t1:NAME:volume:fx;..."` | Play a level sound (e.g. `SE_SM_LV_RABBIT_RUS_HOLE:100:60`) on Mario each frame from t0 to t1 s after boot, as an actor near him would |
| `PETARI_WARP="t:x,y,z;..."` | Put Mario at those world positions t s after boot (zone placements are rotated: `MR::makeMtxTR` order) |
| `PETARI_SWITCH="t:id;..."` | Turn on global stage switch `id` (1000 and up, as placements number them) t s after boot, e.g. `104:1125` opens the Luma's cage on Gateway Galaxy's small planet; `t:Zone/id` turns on switch `id` of that zone, e.g. `102:HeavensDoorInsideZone/0` opens the Grand Star's cage |
| `PETARI_POSLOG=1` | Log the player's position (and whether on the ground) once a second |
| `PETARI_CAMLOG=1` | Log the active game camera (kind, type, chunk), where it watches and where the VR eye is relative to the player twice a second and on camera changes; "blocked" when map geometry lies between the player and the eye |
| `PETARI_STARBITS="t:n"` | Give Mario n star bits t s after boot (to test shooting them) |
| `PETARI_XRSIM_BUDGET=ms` | GPU time allowed per eye in `PETARI_XRSIM`, to exercise the dynamic resolution (without it the scale stays at 1) |
| `PETARI_XRSIM_SWAPSCALE=s` | Size of `PETARI_XRSIM`'s swapchain images relative to the recommended eye size (default the `resolution` setting, at most 1.25), e.g. larger than the render size to time the composite's scaling |
| `PETARI_FIXED_SCALE="t:scale;..."` | Hold the VR render scale at each value from t s after boot on (instead of the dynamic resolution), to time the eyes at each scale; also read from `petari_debug.env` |
| `PETARI_XRSIM_LAYERS=1` | In `PETARI_XRSIM`, send the HUD and settings panels out as UI layers as the headset does, and composite their images into the captures in the compositor's stead |
| `PETARI_XRSIM_TURN="t:dir;..."` | In `PETARI_XRSIM`, snap-turn the diorama t s after boot (the right stick in the headset; dir 1 right, -1 left) |
| `PETARI_XRSIM_STEPS=n`, `PETARI_XRSIM_SMALL=1`, `PETARI_RIGLOG=1` | Display frames simulated per `PETARI_XRSIM` capture (default 40; 1 with `PETARI_XRSIM_FPS` for a continuous sequence); save only the left eye at half size; log diorama rig jumps and fast turns |
| `PETARI_ASYNC=1`, `PETARI_NOCOPY=1` | Use the worker-thread renderer path; perf experiments |
| `PETARI_DLCHECK=1`, `PETARI_NODLCACHE=1` | Decode every draw the display list cache supplies as well and log any difference; turn the cache off |
| `PETARI_XRSIM_AIM="t0-t1:x,y,z[:A];..."`, `PETARI_VRINI=path` | Aim the simulated controller at stage point x,y,z from t0 to t1 s after boot, holding A with `:A` (to work the VR settings panel); the settings file `PETARI_XRSIM` reads and the panel writes |
| `PETARI_PANELLOG=1` | Log the stage point of every control of the VR settings panel (tab by tab), to aim at with `PETARI_XRSIM_AIM` |
| `PETARI_LANGUAGE=name` | The game's language (`french`, `spanish`...) instead of the `language` setting, which the headless runner reads too late (with `PETARI_VRINI`, after the game has started) |

The VR app takes the same variables from `petari_debug.env` (`NAME=value`
lines) next to the game data, in
`/sdcard/Android/data/com.galaxy.quest/files/`, when that file exists:
`PETARI_INPUT` then scripts the controllers from boot, and
`PETARI_SAVE_DIR=<dir>` keeps a test away from the player's saves (files
copied there with adb need `chmod -R 777`, or the game hangs on a black
screen after the strap warning, unable to read them), and
`PETARI_VRSHOT_MS=<ms>` saves both eyes of the headset's picture every
that many ms to `vrshots/` (the headset's own screenshots don't show the
app), with SpaceWarp the left eye's motion vectors as `_mv.png` next to
each, and the virtual screen's layers as `_screen.png` (`_screenL.png` and
`_screenR.png` for a stereo pair). With the proximity sensor overridden (`metavr device proximity
--disable`) a session runs without anyone wearing the headset, as long as
the headset is unlocked. Delete the file afterwards.

Other helpers:

- `tools/pnginfo.py`: capture summary and half-size copies.
- `tools/contact_sheet.py out.png <columns> <png>...`: tiles captures, such as a galaxy tour's, into one image.
- `tools/symbolize_data.py`: map addresses to symbols.
- `tools/find_ptr_casts.py`: find hidden 64-bit pointer truncations.
