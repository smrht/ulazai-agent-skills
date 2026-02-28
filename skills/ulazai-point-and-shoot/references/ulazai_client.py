"""UlazAI point-and-shoot API client.

Minimal wrapper for:
- model discovery
- image generation/status/history
- video studio generation/status/history
- video studio tool endpoints
"""

from __future__ import annotations

import time
from typing import Any, Dict, Optional

import requests


class UlazAIAPIError(Exception):
    """Raised when the UlazAI API returns a non-success response."""

    def __init__(
        self,
        *,
        status_code: int,
        message: str,
        payload: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code
        self.message = message
        self.payload = payload or {}


class UlazAIClient:
    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = "https://ulazai.com",
        timeout_seconds: int = 120,
        session: Optional[requests.Session] = None,
    ) -> None:
        if not api_key or not api_key.strip():
            raise ValueError("api_key is required")

        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds
        self.session = session or requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {api_key.strip()}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "UlazAI-Python-Client/1.0",
            }
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json_body: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_body,
            timeout=self.timeout_seconds,
        )

        try:
            payload = response.json()
        except ValueError:
            payload = {"success": False, "error": response.text or "Invalid JSON response"}

        if response.ok:
            return payload

        error_message = (
            str(payload.get("error") or payload.get("message") or response.reason)
            if isinstance(payload, dict)
            else response.reason
        )
        raise UlazAIAPIError(
            status_code=response.status_code,
            message=error_message,
            payload=payload if isinstance(payload, dict) else None,
        )

    # Model discovery
    def list_image_models(self) -> Dict[str, Any]:
        return self._request("GET", "/api/v1/models/image/")

    def list_video_models(self) -> Dict[str, Any]:
        return self._request("GET", "/api/v1/models/video/")

    # Images
    def generate_image(
        self,
        *,
        prompt: str,
        model: str,
        size: Optional[str] = None,
        quality: Optional[str] = None,
        google_search: Optional[bool] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"prompt": prompt, "model": model}
        if size:
            payload["size"] = size
        if quality:
            payload["quality"] = quality
        if google_search is not None:
            payload.setdefault("input", {})["google_search"] = bool(google_search)
        if extra:
            payload.update(extra)
        return self._request("POST", "/api/v1/generate/", json_body=payload)

    def get_image_status(self, generation_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/api/v1/generate/{generation_id}/")

    def list_image_history(self, *, page: int = 1, limit: int = 20) -> Dict[str, Any]:
        return self._request("GET", "/api/v1/generate/history/", params={"page": page, "limit": limit})

    def wait_for_image(
        self,
        generation_id: str,
        *,
        timeout_seconds: int = 300,
        poll_interval_seconds: float = 2.0,
    ) -> Dict[str, Any]:
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            payload = self.get_image_status(generation_id)
            status_value = str(
                payload.get("status")
                or payload.get("data", {}).get("status")
                or payload.get("generation", {}).get("status")
                or ""
            ).lower()
            if status_value in {"completed", "failed"}:
                return payload
            time.sleep(poll_interval_seconds)
        raise TimeoutError(f"Image generation timed out after {timeout_seconds}s")

    # Videos
    def generate_video(
        self,
        *,
        model_slug: str,
        prompt: str,
        aspect_ratio: Optional[str] = None,
        duration_seconds: Optional[int] = None,
        quality_mode: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        payload: Dict[str, Any] = {"model_slug": model_slug, "prompt": prompt}
        if aspect_ratio:
            payload["aspect_ratio"] = aspect_ratio
        if duration_seconds:
            payload["duration_seconds"] = duration_seconds
        if quality_mode:
            payload["quality_mode"] = quality_mode
        if extra:
            payload.update(extra)
        return self._request("POST", "/api/v1/video-studio/generate/", json_body=payload)

    def get_video_status(self, job_id: str) -> Dict[str, Any]:
        return self._request("GET", f"/api/v1/video-studio/status/{job_id}/")

    def list_video_history(self, *, limit: int = 20) -> Dict[str, Any]:
        return self._request("GET", "/api/v1/video-studio/history/", params={"limit": limit})

    def wait_for_video(
        self,
        job_id: str,
        *,
        timeout_seconds: int = 600,
        poll_interval_seconds: float = 3.0,
    ) -> Dict[str, Any]:
        deadline = time.time() + timeout_seconds
        while time.time() < deadline:
            payload = self.get_video_status(job_id)
            job = payload.get("job", {}) if isinstance(payload, dict) else {}
            status_value = str(job.get("status") or payload.get("status") or "").lower()
            if status_value in {"completed", "failed"}:
                return payload
            time.sleep(poll_interval_seconds)
        raise TimeoutError(f"Video generation timed out after {timeout_seconds}s")

    # Video tools
    def generate_street_interview(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "POST",
            "/api/v1/video-studio/tools/street-interview/generate/",
            json_body=payload,
        )

    def generate_ugc_ad_quick(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "POST",
            "/api/v1/video-studio/tools/ugc-ad-quick/generate/",
            json_body=payload,
        )

    def generate_video_remix(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self._request(
            "POST",
            "/api/v1/video-studio/tools/video-remix/generate/",
            json_body=payload,
        )
