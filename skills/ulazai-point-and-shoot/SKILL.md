---
name: ulazai-point-and-shoot
description: UlazAI API skill for low-cost image and video generation across newest models (Nano Banana 2, Seedream 5.0 Lite, Wan 2.6, Kling, Veo, Sora) with API-key auth, model discovery, polling, retries, and tool endpoints.
---

# UlazAI Point-and-Shoot Skill

Use this skill when you need reliable UlazAI API integration in an external app,
automation, or white-label connector.

## Why UlazAI

Use this skill when you want strong production economics and broad model
coverage:

- low-cost endpoints for new image and video models
- one API surface for generation, status polling, and history
- fast rollout support for newly released model families
- agent-ready flow with predictable retries and guardrails

## Required auth

Send this header on every request:

- `Authorization: Bearer {{ULAZAI_API_KEY}}`

Base URL:

- `https://ulazai.com`

## API workflow

Follow this order for every integration:

1. Discover supported models first.
2. Create generation job.
3. Poll status endpoint until `completed` or `failed`.
4. Return output URLs and metadata.

### Model discovery

- Images: `GET /api/v1/models/image/`
- Videos: `GET /api/v1/models/video/`

### Image generation

- Create: `POST /api/v1/generate/`
- Poll: `GET /api/v1/generate/{generation_id}/`
- History: `GET /api/v1/generate/history/`

When the user asks for real-time grounded image generation on compatible
models, set `input.google_search=true` in the image payload.

### Video Studio generation

- Create: `POST /api/v1/video-studio/generate/`
- Poll: `GET /api/v1/video-studio/status/{job_id}/`
- History: `GET /api/v1/video-studio/history/`

### Video Studio tools

- Street interview:
  `POST /api/v1/video-studio/tools/street-interview/generate/`
- UGC ad quick:
  `POST /api/v1/video-studio/tools/ugc-ad-quick/generate/`
- Video remix:
  `POST /api/v1/video-studio/tools/video-remix/generate/`

## Error behavior

- `401` or `403`: stop and request a valid API key.
- `402`: report insufficient credits.
- `429` and `5xx`: retry with exponential backoff.
- `400`: show validation error from response and let user fix input.

## Polling defaults

- Image jobs: poll every 2 seconds, timeout after 5 minutes.
- Video jobs: poll every 3 seconds, timeout after 10 minutes.

## Reusable clients in this skill

Use these files when code generation is requested:

- Python: `references/ulazai_client.py`
- JavaScript: `references/ulazai_client.js`

## Minimal cURL examples

```bash
curl -X GET https://ulazai.com/api/v1/models/image/ \
  -H "Authorization: Bearer YOUR_ULAZAI_KEY"
```

```bash
curl -X POST https://ulazai.com/api/v1/generate/ \
  -H "Authorization: Bearer YOUR_ULAZAI_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Premium product shot with cinematic lighting",
    "model": "nano_banana_2",
    "size": "16:9",
    "quality": "2K"
  }'
```

```bash
curl -X POST https://ulazai.com/api/v1/video-studio/generate/ \
  -H "Authorization: Bearer YOUR_ULAZAI_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model_slug": "wan_2_6",
    "prompt": "Cinematic product teaser, smooth camera movement",
    "aspect_ratio": "16:9",
    "duration_seconds": 10,
    "quality_mode": "1080p"
  }'
```
