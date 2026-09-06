---
type: canonical
source: none
sync: none
sla: none
authority: canonical
audience: [ai-agents, contributors]
last_updated: 2026-09-06
last-verified: 2026-09-06
---

# CLAUDE.md: SpinCirc

Universal agent rules and simplicity defaults live in [AGENTS.md](AGENTS.md). Read that first.

## Claude-specific deltas

Shared voice and research-writing contract:

- <https://github.com/alawein/alawein/blob/main/docs/style/VOICE.md>
- <https://github.com/alawein/alawein/blob/main/prompt-kits/AGENT.md>

### Docker

`Dockerfile` and `docker-compose.yml` define a `test-runner` service:

```bash
docker compose run --rm test-runner
```

Other compose services include `spincirc`, `jupyter`, `python-dev`, `docs`, and `dev`. See `build-docker.sh` and `docker/` for image build details.
