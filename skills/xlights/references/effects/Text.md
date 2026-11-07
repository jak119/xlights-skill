# Text effect

XML: `<Effect name="Text" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_TEXTCTRL_Text` | string |  |  | The text string to display. Supports multiple lines and special tokens for countdown modes. When non-empty, the file picker and lyric track are disabled. |
| `E_CHOICE_Text_LyricTrack` | enum |  | (dynamic: lyricTimingTracks) | Selects a lyric timing track to use as the text source. The current lyric phrase or word is displayed at each point in time. Disabled when Text or From File is set. |
| `E_FONTPICKER_Text_Font` | font |  |  | The font face, size, and style used to render the text. |
| `E_CHOICE_Text_Dir` | enum | none | none, left, right, up, down, vector, up-left, down-left, up-right, down-right, wavey, word-flip, left-right, up-down | Direction the text moves across the model. Options include scrolling left/right/up/down, diagonal, wavey motion, word-flip, and vector-based movement between start and end positions. |
| `E_CHECKBOX_TextToCenter` | bool | 0 |  | When enabled, the text movement stops when the text reaches the center of the model rather than continuing off screen. Only meaningful when Movement is not 'none'. |
| `E_CHECKBOX_TextNoRepeat` | bool | 0 |  | When enabled, the text scrolls through once and then stops instead of repeating in a loop. Only meaningful when Movement is not 'none'. |
| `E_TEXTCTRL_Text_Speed` | int | 10 | 0 .. 100 | How fast the text scrolls across the model. Higher values produce faster movement. |
| `E_CHOICE_Text_Effect` | enum | normal | normal, vert text up, vert text down, rotate up 45, rotate up 90, rotate down 45, rotate down 90 | Text rendering style. Normal draws text horizontally; other options rotate or orient the text vertically. |
| `E_CHOICE_Text_Count` | enum | none | none, seconds, minutes seconds, to date 'd h m s', to date 'h:m:s', to date 'm' or 's', to date 's', !to date!%fmt | Enables countdown mode. The text field value is used as the target, and the displayed text shows the remaining time in the selected format. |
| `E_CHECKBOX_Text_PixelOffsets` | bool | 0 |  | When enabled, the X and Y position values are interpreted as pixel offsets rather than percentage-based positions. |
| `E_CHECKBOX_Text_Color_PerWord` | bool | 0 |  | When enabled, each word in the text is drawn using a different color from the palette, cycling through the available colors. |
| `E_SLIDER_Text_XStart` | int | 0 | -200 .. 200 | Horizontal starting position of the text. Used as the origin for vector movement or as a static offset when movement is none. |
| `E_SLIDER_Text_YStart` | int | 0 | -200 .. 200 | Vertical starting position of the text. Used as the origin for vector movement or as a static offset when movement is none. |
| `E_SLIDER_Text_XEnd` | int | 0 | -200 .. 200 | Horizontal ending position for vector movement mode. The text moves from the start position to this position over the effect duration. |
| `E_SLIDER_Text_YEnd` | int | 0 | -200 .. 200 | Vertical ending position for vector movement mode. The text moves from the start position to this position over the effect duration. |
| `E_FILEPICKERCTRL_Text_File` | file |  |  | Text file to display instead of E_TEXTCTRL_Text. |
| `E_CHOICE_Text_Font` | enum | Use OS Fonts | (dynamic: xlFonts) | xLights bitmap font, or 'Use OS Fonts' to use E_FONTPICKER_Text_Font. |

## Custom controls (set these in the xLights UI if possible)

- `Text_File_Row`: Path to a text file whose contents are displayed instead of the text field. Each line in the file is treated as a separate text line. Disabled when the Text field above is non-empty.
- `Text_Font_XL_Row`: Selects an xLights bitmap font (under fonts/) to use instead of the OS font. 'Use OS Fonts' falls back to the Font picker above.

## Visibility rules (which settings matter when)

- when `Text_Dir != 'none'`: enable TextToCenter, TextNoRepeat
- when `Text_Dir == 'none'`: disable TextToCenter, TextNoRepeat
- when `Text != ''`: disable Text_File_Row, Text_LyricTrack
- when `Text_File_Row != ''`: disable Text_LyricTrack
