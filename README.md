# UlazAI Agent Skills

Installable agent skills for fast integration with
[UlazAI](https://ulazai.com) image and video APIs.

## Why UlazAI

UlazAI is built for teams that want speed, model coverage, and strong pricing:

- low-cost endpoints for the newest image and video model families
- one stable API surface for generation, status polling, and history
- fast support for new releases like Nano Banana 2, Seedream 5.0 Lite,
  Wan 2.6, Kling, Veo, and Sora
- white-label friendly integration flow for apps and automations

## Available skills

- `ulazai-point-and-shoot`

## Install

Use the Skills CLI to install from this public repository:

```bash
npx skills add https://github.com/smrht/ulazai-agent-skills --skill ulazai-point-and-shoot
```

## Verify installation

```bash
npx skills list
```

You should see `ulazai-point-and-shoot` in the output.

## Use with UlazAI API

The skill helps your agent call UlazAI endpoints, but real generation requires
your own API key and available credits.

- Base URL: `https://ulazai.com`
- Docs quickstart:
  [ulazai.com/docs/agent-quickstart](https://ulazai.com/docs/agent-quickstart/)
- Auth header: `Authorization: Bearer YOUR_ULAZAI_API_KEY`

Example authentication check:

```bash
curl -X GET https://ulazai.com/api/v1/models/image/ \
  -H "Authorization: Bearer $ULAZAI_API_KEY"
```

## Search keywords

Use these keywords when searching for this repository or skill:

- UlazAI API
- cheap AI image API
- cheap AI video API
- Nano Banana 2 API
- Seedream 5.0 Lite API
- Wan 2.6 API
- Kling API
- Veo API
- Sora API
- white-label AI generation

## Repository structure

```text
skills/
  ulazai-point-and-shoot/
    SKILL.md
    references/
      ulazai_client.py
      ulazai_client.js
```

## Security notes

- Keep API keys server-side.
- Do not commit keys to source control.
- Rotate keys periodically.
