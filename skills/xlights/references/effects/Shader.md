# Shader effect

XML: `<Effect name="Shader" .../>`. Settings go in `<EffectDB>`; colours in `<ColorPalettes>`.

## Settings

| Key | Type | Default | Range / options | Notes |
|---|---|---|---|---|
| `E_TEXTCTRL_Shader_LeadIn` | int | 0 | 0 .. 1000 | Number of frames to pre-render before the effect starts, allowing time-based shaders to reach a desired visual state at the beginning of the effect. |
| `E_TEXTCTRL_Shader_Offset_X` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_Shader_Offset_X`] Horizontal offset of the shader viewport as a percentage. Only active for shaders that consume iResolution / coordinate uniforms. |
| `E_TEXTCTRL_Shader_Offset_Y` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_Shader_Offset_Y`] Vertical offset of the shader viewport as a percentage. Only active for shaders that consume iResolution / coordinate uniforms. |
| `E_TEXTCTRL_Shader_Zoom` | int | 0 | -100 .. 100 | [VC: `E_VALUECURVE_Shader_Zoom`] Zoom level for the shader output. Positive values zoom in, negative values zoom out, and zero shows the shader at its native scale. Only active for shaders that consume iResolution / coordinate uniforms. |

## Custom controls (set these in the xLights UI if possible)

- `Shader_FilenameBlock`: Custom block with Select/Clear/Download buttons, animated shader preview, and filename label. The shader file path is serialized as E_0FILEPICKERCTRL_IFS via a hidden file picker; the leading 0 forces it to be processed first at load time so the shader config is known before dynamic uniform settings are applied.
- `Shader_SpeedRow`: Custom Time Speed slider row. Built as a BulkEditSliderF2 with the slider as the serialized control (E_SLIDER_Shader_Speed, divisor 100) and a buddy text control, matching the legacy naming so old sequences continue to deserialize.
- `Shader_DynamicParams`: Container for per-shader dynamic uniform controls. ShaderPanel reserves the sizer here; ShaderConfig::GetDynamicPropertiesJson emits a schema-shaped JSON array for every visible uniform, and the JsonEffectPanel builder renders the rows so iPad and desktop share the same layout logic. The sizer is wiped (and its PropertyInfo entries purged via RemovePropertiesWithPrefix) whenever the shader file changes.
