from dataclasses import dataclass

from web_readiness_analyzer.rules import DESKTOP_WEB, MOBILE_AR


@dataclass(frozen=True)
class OptimizationPreset:
    key: str
    texture_size: int
    texture_compress: str
    geometry_compress: str
    meshopt_level: str


MOBILE_PRESET = OptimizationPreset(
    key=MOBILE_AR.key,
    texture_size=MOBILE_AR.max_texture_resolution,
    texture_compress="auto",
    geometry_compress="meshopt",
    meshopt_level="high",
)

DESKTOP_PRESET = OptimizationPreset(
    key=DESKTOP_WEB.key,
    texture_size=DESKTOP_WEB.max_texture_resolution,
    texture_compress="auto",
    geometry_compress="meshopt",
    meshopt_level="high",
)

OPTIMIZATION_PRESETS = {
    MOBILE_PRESET.key: MOBILE_PRESET,
    DESKTOP_PRESET.key: DESKTOP_PRESET,
}


def get_optimization_preset(profile_key: str) -> OptimizationPreset:
    try:
        return OPTIMIZATION_PRESETS[profile_key]
    except KeyError as error:
        available = ", ".join(OPTIMIZATION_PRESETS)
        raise ValueError(
            f"Unknown optimization profile '{profile_key}'. "
            f"Available profiles: {available}"
        ) from error
