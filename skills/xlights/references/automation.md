# Automating xLights: command line, REST API, MCP

There are two ways an agent can change a show:
1. **Edit files** (`.xsq`, layout XML) while xLights does **not** have them open, then render.
2. **Drive a running xLights** through its automation API, so xLights does the editing, saving, and
   rendering itself. This is safer when the user has xLights open.

## Command line (verified with xLights 2026.19 `--help`)

| Flag | Purpose |
|---|---|
| `-hl`, `--headless` | Render sequence(s) to `.fseq` with **no window**, then exit. Exit code `0` = OK, `1` = render/write error, `2` = bad args. |
| `-s`, `--show=DIR` | Show folder (required for headless). |
| `-m`, `--media=DIR` | Media folder. |
| `-od`, `--outputdir=DIR` | Where to write `.fseq` (default: the show's configured FSEQ folder, often the show folder). |
| `-r`, `--render` | Render with the desktop app and exit. |
| `-cs`, `--checksequence` | Run Check Sequence and exit. |
| `-fc`, `--fseqcmp A B` | Compare two `.fseq` files (exit 0 = identical); with `-s`, gives per-model differences. |

```bash
# macOS
/Applications/xLights.app/Contents/MacOS/xLights --headless -s "/path/Show" "/path/Show/Song.xsq"
# Windows
"C:\Program Files\xLights\xLights.exe" --headless -s "C:\Show" "C:\Show\Song.xsq"
# wrapper (auto-finds the binary)
python3 scripts/xsq.py render "/path/Show/Song.xsq" --show "/path/Show"
```

Notes:
- **macOS sandbox**: the app can only read folders the user has opened in xLights (bookmarked). Keep
  sequences inside the show folder. Temp folders like `/tmp` won't work.
- Headless rendering works while the GUI is also running, but it writes the same `.fseq`. If the GUI then
  re-renders, it overwrites it.
- Read the log for problems: macOS `~/Library/Containers/org.xlights/Data/Library/Logs/xLights_spdlog.log`.
  Look for "Effect dropped", "not found", or "Settings ignored". A clean open logs
  `HeadlessRenderContext: opened ... (N elements, M ms long)`.
- To prove effects render (not just that the file loads), render an empty copy of the sequence and run
  `--fseqcmp -s SHOW a.fseq b.fseq`. Models with effects should show differences.

## REST API (xFade port)

Enable the xFade/automation port in xLights preferences. It listens on **http://127.0.0.1:49913**
(A) or 49914 (B). The docs call it **experimental**. Main endpoints:

```
GET  /getVersion                GET /getShowFolder            GET /openSequence          (current)
GET  /openSequence/<file.xsq>?force=true                      GET /closeSequence?force=true
GET  /newSequence?duration=60&frameMS=50&view=All%20Models    GET /saveSequence?seq=<name>
GET  /renderAll                 GET /batchRender?seq_0=<a>&seq_1=<b>
GET  /checkSequence             GET /uploadController         GET /uploadSequence
GET  /lightsOn  /lightsOff      GET /getMedia  /getMediaIssues  /embedMedia  /extractMedia
POST /xlDoAutomation            body: {"cmd": "...", ...}   (every command below)
POST /mcp                       MCP server (below)
```

GET parameters need spaces escaped as `%20` and can't contain `/`. Use `POST /xlDoAutomation` with JSON
for anything with paths.

### Useful `xlDoAutomation` commands

```json
{"cmd":"getModels","models":"true","groups":"true"}
{"cmd":"loadSequence","seq":"Song.xsq","promptIssues":"false"}
{"cmd":"newSequence","force":"true","mediaFile":"Audio/song.mp3","durationSecs":185,"frameMS":50,"view":"All Models"}
{"cmd":"addEffect","target":"Mega Tree","effect":"Bars","settings":"E_CHOICE_Bars_Direction=up","palette":"C_BUTTON_Palette1=#FF0000,C_CHECKBOX_Palette1=1","layer":"0","startTime":"0","endTime":"5000"}
{"cmd":"getEffectIDs","model":"Mega Tree"}
{"cmd":"getEffectSettings","model":"Mega Tree","layer":"0","id":"0"}
{"cmd":"setEffectSettings","model":"Mega Tree","layer":"0","id":"0","name":"On","palette":{"C_BUTTON_Palette1":"#0000FF","C_CHECKBOX_Palette1":"1"},"settings":{"E_TEXTCTRL_Eff_On_Start":"10"},"startTime":"10","endTime":"100"}
{"cmd":"deleteEffect","model":"Mega Tree","layer":"0","id":"0"}
{"cmd":"cloneModelEffects","target":"Arch 2","source":"Arch 1","eraseModel":"true"}
{"cmd":"clearModelEffects","model":"Mega Tree"}
{"cmd":"saveSequence"}
{"cmd":"renderAll","highdef":"false"}
{"cmd":"checkSequence","seq":"Song.xsq"}
{"cmd":"getSequenceInfo","filename":"/path/Show/Song.xsq"}
{"cmd":"listSequences","folder":"/path/Show"}
{"cmd":"importXLightsSequence","filename":"vendor.xsq","mapmethod":"auto"}
{"cmd":"exportModelWithRender","filename":"out.mp4","model":"Matrix","format":"mp4compressed"}
{"cmd":"runScript","filename":"script.lua"}
```

Responses look like `{"res":200,"msg":"...","worked":"true"}`. The full list is in the xLights repo,
`documentation/xlDo Commands.txt`.

### MCP server (newer builds)

`POST http://127.0.0.1:49913/mcp` speaks stateless MCP over HTTP (JSON-RPC 2.0: `initialize`, `tools/list`,
`tools/call`). It offers a generic `xlights_command` tool (cmd + params, covering every command above)
and convenience tools: `getVersion`, `openSequence`, `saveSequence`, `closeSequence`, `renderAll`,
`getModels`, `getControllers`, `get/set/add/deleteEffect`, `lightsOn/lightsOff`. If the user's client
supports HTTP MCP servers, they can register it. Check `getVersion` first, since older xLights builds lack
`/mcp`.

Caution: `lightsOn`, `uploadController`, `uploadSequence`, `uploadFPPConfig` and `changeShowFolder`
affect real hardware or the user's setup. Ask before calling them.

## Lua scripts

xLights has a Script Runner that runs Lua with `RunCommand(cmd, params)` (the same commands as
xlDoAutomation), plus prompts (`PromptSequences`, `PromptSelection`, …) and `Log`. Scripts live in the show
folder's scripts directory. They're useful for repeatable batch jobs the user runs themselves.

## Choosing an approach

| Situation | Approach |
|---|---|
| xLights closed, big generative change | Edit `.xsq` with `xsq.py`, validate, headless render |
| xLights open on that sequence | Automation API (`addEffect`, `saveSequence`, `renderAll`), or ask the user to close it |
| Need the user to see it | Edit the file, then have them open it (or `loadSequence` via API) |
| Bulk render or check many songs | `--headless` with a glob, or `batchRender` |
