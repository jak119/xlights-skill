# Falcon Player (FPP): playing the show

**FPP (Falcon Player)** is the most popular way to run an xLights show. It's free software, usually on a
Raspberry Pi or BeagleBone (and built into many pixel controllers). It plays rendered `.fseq` files
(plus audio) on a schedule, so the computer running xLights doesn't need to be on during the show.
xLights designs and renders; FPP plays.

```
xLights (design) --render--> Song.fseq --FPP Connect upload--> FPP (playlists + schedule) --> controllers --> pixels
```

## Key ideas

- **FPP plays `.fseq`, not `.xsq`.** Every sequence change needs **re-render, then re-upload**. A common
  "my change didn't show up" cause is forgetting the upload.
- **Audio** (`.mp3`/`.wav`/`.mp4`) is uploaded separately as media. Only the FPP that plays the audio
  needs it. Animations have no media.
- **Playlists** group sequences in order (lead-in, songs or animations, lead-out) and can repeat.
- **Scheduler** starts playlists at set times (for example 5:30–10:00 pm nightly, or "sunset" to a time).
- **Modes** (FPP version dependent): a **player** runs the show. **Remote** units play their own copy of
  the `.fseq` in sync with the player (handy for distant props). Some FPP-based controllers just drive
  their own outputs.
- **UDP output vs. local outputs**: FPP can send pixel data over the network (E1.31/DDP/ArtNet) to your
  controllers, and/or drive pixels directly through a Pi hat or cape.

## Sending to FPP from xLights: FPP Connect

xLights's **FPP Connect** dialog discovers FPP devices on the network and uploads to them. Its options,
paraphrased from the dialog's own tooltips (xLights 2026.19):

| Option | What it does |
|---|---|
| Upload | Enable uploading files/configs to this FPP device. |
| Media | Upload the MP3/MP4/WAV for each sequence. Suggested only on the FPP that plays your audio. |
| UDP Out | `None`: this FPP won't send pixel data. `All`: sends to every controller marked ACTIVE. `Proxied`: only controllers proxied through this FPP. |
| Add Proxies | Adds proxy settings to the FPP automatically. |
| Upload Outputs | Pushes the latest inputs/outputs from xLights's controller setup. **May restart FPPD and disrupt a running show.** |
| FSEQ Type | File version. **V2 Sparse/zstd is recommended** unless a device doesn't support it (then try V2 zlib or uncompressed). |
| Models | Uploads models for display testing on FPP. Typically not needed; **restarts FPPD**. |
| Playlist | Adds the uploaded sequences to the chosen FPP playlist. |

xLights checks which sequences and media are out of date and only sends those.

**Agent guidance:** uploading changes what plays on real hardware, and some options restart the player.
Tell the user what will be uploaded and with which options, and let them run FPP Connect (or get explicit
approval before using the automation commands below). Avoid output and model uploads during show hours.

### The same thing by automation (experimental API)

```json
{"cmd":"uploadSequence", "ip":"192.168.1.100", "seq":"Song.xsq", "media":"true", "format":"v2std"}
{"cmd":"uploadFPPConfig", "ip":"192.168.1.100", "udp":"all", "models":"false", "map":"false"}
```

`format` options: `v1`, `v2std`, `v2zlib`, `v2uncompressed`, `v2stdsparse`, `v2zlibsparse`,
`v2uncompressedsparse`. `models:true` uploads models; `map:true` uploads the virtual display map
(FPP's preview). See `automation.md` for how to call these.

## Typical setups

- **Animation-only display** (see `animations-and-ambient.md`): render a few looping animations, upload
  without media, put them in one playlist set to repeat, and schedule it nightly.
- **Musical show**: upload with media to the audio-playing FPP. Build a playlist with lead-in/out, songs,
  and maybe an animation loop between shows. Schedule show times. Audio usually goes to an FM transmitter
  or speakers attached to the FPP.
- **Mixed**: an ambient animation playlist on repeat most of the evening, plus scheduled musical show
  times. FPP's scheduler handles the switch.

## Troubleshooting checklist

| Symptom | Likely cause |
|---|---|
| Changes not visible | Not re-rendered, or not re-uploaded (check the FSEQ timestamps in FPP Connect). |
| Lights don't light during playback | UDP Out set to `None`, controller not ACTIVE, or outputs not uploaded. |
| Some props dark | That controller's IP or universes don't match xLights; a remote isn't in sync or lacks the file. |
| Audio but no lights (or the reverse) | Media uploaded to the wrong FPP; playlist entry is media-only or sequence-only. |
| Upload fails | FPP unreachable or the wrong IP; check FPP's web UI on that IP. An older FPP may not support the chosen FSEQ type. |
| Stutter or lag | Network too busy or Wi-Fi; prefer a wired show network. Sparse/zstd files reduce load. |

Playlists, schedules, and FPP's own settings live in **FPP's web interface** (browse to its IP address).
xLights only adds sequences to a playlist. Guide the user there for schedules and repeat settings.
