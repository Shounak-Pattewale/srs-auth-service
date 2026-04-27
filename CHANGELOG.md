# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-04-27

### Added
- JWT encode/decode utilities (`create_token`, `decode_token`)
- Password hashing/verification (`hash_password`, `verify_password`)
- FastAPI dependency factories (`make_get_current_user`, `make_require_role`)
- FastAPI middleware guards (`make_role_guard`, `make_tenant_guard`)
- Flask role decorator (`role_required`)
- Test suite with 15 passing tests

### Changed
- Initial release
