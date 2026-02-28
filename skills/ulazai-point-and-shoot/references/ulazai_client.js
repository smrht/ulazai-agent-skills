/**
 * UlazAI point-and-shoot API client.
 *
 * Works in Node 18+ and modern browsers that support fetch.
 */

export class UlazAIAPIError extends Error {
  constructor(statusCode, message, payload = {}) {
    super(`HTTP ${statusCode}: ${message}`);
    this.name = "UlazAIAPIError";
    this.statusCode = statusCode;
    this.payload = payload;
  }
}

export class UlazAIClient {
  constructor({ apiKey, baseUrl = "https://ulazai.com", timeoutMs = 120000 } = {}) {
    if (!apiKey || !String(apiKey).trim()) {
      throw new Error("apiKey is required");
    }

    this.apiKey = String(apiKey).trim();
    this.baseUrl = String(baseUrl).replace(/\/+$/, "");
    this.timeoutMs = timeoutMs;
  }

  async request(method, path, { params, body } = {}) {
    const url = new URL(`${this.baseUrl}${path}`);
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null && value !== "") {
          url.searchParams.set(key, String(value));
        }
      });
    }

    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), this.timeoutMs);

    let response;
    let payload;
    try {
      response = await fetch(url, {
        method,
        headers: {
          Authorization: `Bearer ${this.apiKey}`,
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: body ? JSON.stringify(body) : undefined,
        signal: controller.signal,
      });

      const raw = await response.text();
      try {
        payload = raw ? JSON.parse(raw) : {};
      } catch {
        payload = { success: false, error: raw || "Invalid JSON response" };
      }
    } finally {
      clearTimeout(timeout);
    }

    if (response.ok) {
      return payload;
    }

    const message = payload?.error || payload?.message || response.statusText || "Request failed";
    throw new UlazAIAPIError(response.status, message, payload);
  }

  // Model discovery
  listImageModels() {
    return this.request("GET", "/api/v1/models/image/");
  }

  listVideoModels() {
    return this.request("GET", "/api/v1/models/video/");
  }

  // Images
  generateImage({ prompt, model, size, quality, googleSearch, extra = {} }) {
    const payload = { prompt, model, ...extra };
    if (size) payload.size = size;
    if (quality) payload.quality = quality;
    if (googleSearch !== undefined) {
      payload.input = { ...(payload.input || {}), google_search: Boolean(googleSearch) };
    }
    return this.request("POST", "/api/v1/generate/", { body: payload });
  }

  getImageStatus(generationId) {
    return this.request("GET", `/api/v1/generate/${generationId}/`);
  }

  listImageHistory({ page = 1, limit = 20 } = {}) {
    return this.request("GET", "/api/v1/generate/history/", { params: { page, limit } });
  }

  async waitForImage(generationId, { timeoutMs = 300000, pollMs = 2000 } = {}) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      const payload = await this.getImageStatus(generationId);
      const status = String(
        payload?.status || payload?.data?.status || payload?.generation?.status || ""
      ).toLowerCase();
      if (status === "completed" || status === "failed") {
        return payload;
      }
      await new Promise((resolve) => setTimeout(resolve, pollMs));
    }
    throw new Error(`Image generation timed out after ${timeoutMs}ms`);
  }

  // Videos
  generateVideo({
    modelSlug,
    prompt,
    aspectRatio,
    durationSeconds,
    qualityMode,
    extra = {},
  }) {
    const payload = { model_slug: modelSlug, prompt, ...extra };
    if (aspectRatio) payload.aspect_ratio = aspectRatio;
    if (durationSeconds) payload.duration_seconds = durationSeconds;
    if (qualityMode) payload.quality_mode = qualityMode;
    return this.request("POST", "/api/v1/video-studio/generate/", { body: payload });
  }

  getVideoStatus(jobId) {
    return this.request("GET", `/api/v1/video-studio/status/${jobId}/`);
  }

  listVideoHistory({ limit = 20 } = {}) {
    return this.request("GET", "/api/v1/video-studio/history/", { params: { limit } });
  }

  async waitForVideo(jobId, { timeoutMs = 600000, pollMs = 3000 } = {}) {
    const deadline = Date.now() + timeoutMs;
    while (Date.now() < deadline) {
      const payload = await this.getVideoStatus(jobId);
      const status = String(payload?.job?.status || payload?.status || "").toLowerCase();
      if (status === "completed" || status === "failed") {
        return payload;
      }
      await new Promise((resolve) => setTimeout(resolve, pollMs));
    }
    throw new Error(`Video generation timed out after ${timeoutMs}ms`);
  }

  // Video tools
  generateStreetInterview(payload) {
    return this.request("POST", "/api/v1/video-studio/tools/street-interview/generate/", {
      body: payload,
    });
  }

  generateUgcAdQuick(payload) {
    return this.request("POST", "/api/v1/video-studio/tools/ugc-ad-quick/generate/", {
      body: payload,
    });
  }

  generateVideoRemix(payload) {
    return this.request("POST", "/api/v1/video-studio/tools/video-remix/generate/", {
      body: payload,
    });
  }
}
