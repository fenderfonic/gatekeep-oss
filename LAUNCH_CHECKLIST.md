# Launch Checklist

Use this to verify everything is ready before publishing to PyPI and announcing.

## Pre-Launch (Do Once)

- [x] All tests passing (65/65)
- [x] Lint clean (ruff)
- [x] Format clean (ruff format)
- [x] Package builds (sdist + wheel)
- [x] README complete with install instructions
- [x] LICENSE file (MIT)
- [x] CONTRIBUTING.md
- [x] SECURITY.md
- [x] CHANGELOG.md
- [x] GitHub funding setup (.github/FUNDING.yml)
- [x] CI/CD workflow (.github/workflows/ci.yml)
- [x] Issue templates
- [x] PR template

## GitHub Setup

- [ ] Create GitHub repo: `fenderfonic/gatekeep-oss`
- [ ] Push code to GitHub
- [ ] Add description: "AI-powered governance that explains the why behind best practices"
- [ ] Add topics: `governance`, `security`, `ai`, `code-review`, `compliance`, `python`, `cli`
- [ ] Enable GitHub Sponsors (if not already)
- [ ] Create Buy Me a Coffee account (if not already)
- [ ] Update FUNDING.yml with correct usernames

## PyPI Publishing

- [ ] Create PyPI account (if needed)
- [ ] Generate API token
- [ ] Test publish to TestPyPI first:
  ```bash
  python -m build
  twine upload --repository testpypi dist/*
  ```
- [ ] Verify TestPyPI package works:
  ```bash
  pip install --index-url https://test.pypi.org/simple/ gatekeep
  ```
- [ ] Publish to real PyPI:
  ```bash
  twine upload dist/*
  ```
- [ ] Verify: `pip install gatekeep`

## Post-Launch Announcement

- [ ] Post on Hacker News: "Show HN: Gatekeep – AI governance that teaches security/cost/compliance as you code"
- [ ] Post on Reddit: r/programming, r/python
- [ ] Tweet about it (if you use Twitter)
- [ ] Post in relevant Discord/Slack communities
- [ ] Email friends who might be interested

## Monitoring (First Week)

- [ ] Watch GitHub issues for bugs
- [ ] Monitor PyPI download stats
- [ ] Respond to questions/feedback quickly
- [ ] Track feature requests in ROADMAP.md
- [ ] Update README based on common questions

## Success Metrics

Track these weekly:
- GitHub stars
- PyPI downloads
- GitHub issues (open/closed)
- Sponsor count
- Community engagement

## If Things Go Wrong

**Common issues:**
- Package doesn't install → Check dependencies in pyproject.toml
- CLI doesn't work → Verify entry points in pyproject.toml
- Tests fail on user's machine → Check Python version compatibility
- API key errors → Improve error messages and docs

**Stay calm:**
- Bugs are normal
- Users are helpful
- Fix fast, communicate clearly
- Learn and iterate

## Remember

- You don't need 1000 stars to be successful
- Even 10 happy users is a win
- Focus on helping people, not metrics
- Have fun with it

**You've built something real. Now ship it and see what happens.**
