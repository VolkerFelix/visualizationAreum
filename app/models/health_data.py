from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional


@dataclass
class AccelerationSample:
    timestamp: datetime
    x: float
    y: float
    z: float


@dataclass
class DeviceInfo:
    device_type: str
    model: str
    os_version: str
    device_id: Optional[str] = None


@dataclass
class AccelerationData:
    id: str
    data_type: str
    device_info: DeviceInfo
    sampling_rate_hz: int
    start_time: datetime
    samples: List[AccelerationSample]
    created_at: datetime
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class ActivityMetrics:
    avg_intensity: float
    duration: float
    active_samples: int
    peak_magnitude: float
