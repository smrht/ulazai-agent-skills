# UlazAI Agent Skills

Installable agent skills for fast integration with
[UlazAI](https://ulazai.com) image and video APIs.

## Available skills

- `ulazai-point-and-shoot`

This skill is designed for agents that need a reliable flow for:

- model discovery
- image generation and polling
- video generation and polling
- video tool endpoints

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
- Docs quickstart: [ulazai.com/docs/agent-quickstart](https://ulazai.com/docs/agent-quickstart/)
- Auth header: `Authorization: Bearer YOUR_ULAZAI_API_KEY`

Example authentication check:

```bash
curl -X GET https://ulazai.com/api/v1/models/image/ \
  -H "Authorization: Bearer $ULAZAI_API_KEY"
```

## Repository structure

```text
skills/
  ulazai-point-and-shoot/
    SKILL.md
    references/
      ulazai_client.py
      ulazai_client.js
```

## Notes

- Keep API keys server-side.
- Do not commit keys to source control.
- Rotate keys periodically.
