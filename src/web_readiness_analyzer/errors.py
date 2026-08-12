class AssetProcessingError(RuntimeError):
    """Base error for failures while processing an asset."""


class ToolExecutionError(AssetProcessingError):
    """An external tool finished unsuccessfully."""


class ToolTimeoutError(AssetProcessingError):
    """An external tool exceeded its execution deadline."""
