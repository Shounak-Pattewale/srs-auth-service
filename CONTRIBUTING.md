# Contributing to srs-auth-service

## Development Setup

```bash
git clone https://github.com/Shounak-Pattewale/srs-auth-service.git
cd srs-auth-service
bash setup-dev.sh
source venv/bin/activate
```

## Running Tests

```bash
pytest -v
```

## Code Style

- Follow PEP 8 guidelines
- Type hints required for all functions
- No fluff or filler in comments

## Commit Messages

Use conventional commit format:

- `feat: add new feature`
- `fix: bug fix`
- `docs: update documentation`
- `test: add tests`
- `chore: update dependencies`

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make changes and add tests
4. Run tests (`pytest -v`)
5. Commit with descriptive messages
6. Push to your fork
7. Open a pull request

## Release Process

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Build package: `python3 -m build`
4. Test upload: `twine upload --repository testpypi dist/*`
5. Publish: `twine upload dist/*`
