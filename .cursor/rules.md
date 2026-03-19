## AI Rules for rori-marketing

Always read these files before making changes:
- `./AI_CONTEXT.md` — full campaign state, IDs, strategy, token info
- `./MARKETING_LOG.md` — chronological action log
- `./config.py` — all Meta IDs and campaign config
- `../rori-bible/AI_CONTEXT.md` — global Rori platform context
- `../rori-bible/AI_CHANGELOG.md` — recent cross-repo changes

### Rules
1. Never commit `.env` or access tokens to git.
2. After any campaign change, add an entry to `MARKETING_LOG.md`.
3. After any ID change, update `config.py`.
4. All Meta API calls go through `src/` modules, not raw curl.
5. Don't modify paused legacy campaigns — they're historical reference.
6. Don't change campaign budgets by more than 20% at a time.
7. Token renew deadline: check `AI_CONTEXT.md` for expiry date.
