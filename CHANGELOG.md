# CHANGELOG


## v0.1.0 (2026-02-14)

### Chores

- Remove Windows run scripts; prefer shell launcher
  ([`9f20d31`](https://github.com/CharlesW1/Python-Image-Clicker/commit/9f20d3101145933e716c8d2c66dd93dc2e57e660))

Remove Windows-specific run scripts (run_image_clicker.bat and run_image_clicker_from_dist.bat).
  Keep un_image_clicker.sh as the canonical launcher for cross-platform contributors who prefer sh.

### Features

- Add automated versioning and releases via GitHub Actions
  ([`3f6272c`](https://github.com/CharlesW1/Python-Image-Clicker/commit/3f6272c6c0a62a15846e56acae2febb8306226e1))

- Added `pyproject.toml` with `python-semantic-release` configuration. - Initialized versioning in
  `src/clicker/__init__.py`. - Created `.github/workflows/release.yml` for automated releases and
  Windows builds. - Ensured the workflow correctly handles the original script filename. - Addressed
  PR feedback regarding documentation and permissions.

Co-authored-by: CharlesW1 <8813880+CharlesW1@users.noreply.github.com>

- Add automated versioning and releases via GitHub Actions
  ([`6945305`](https://github.com/CharlesW1/Python-Image-Clicker/commit/6945305f8c326bc04e7065e7018b6dafdf040439))

- Added `pyproject.toml` with `python-semantic-release` configuration. - Initialized versioning in
  `src/clicker/__init__.py`. - Created `.github/workflows/release.yml` for automated versioning and
  Windows builds. - Kept the original entry point filename `Image-Clicker(v1.2).py` as requested. -
  Updated build and release scripts to handle the original filename with parentheses.

Co-authored-by: CharlesW1 <8813880+CharlesW1@users.noreply.github.com>

- Add automated versioning and releases via GitHub Actions
  ([`38f2f48`](https://github.com/CharlesW1/Python-Image-Clicker/commit/38f2f4821e776d1b9a021b0891a9cf8b28429edb))

- Renamed entry point to `image_clicker.py` for a stable filename. - Initialized versioning in
  `src/clicker/__init__.py`. - Added `pyproject.toml` with `python-semantic-release` configuration.
  - Created `.github/workflows/release.yml` for automated versioning and Windows builds. - Updated
  all references in documentation and scripts.

Co-authored-by: CharlesW1 <8813880+CharlesW1@users.noreply.github.com>

### Refactoring

- Consolidate clicker modules into src/clicker and remove legacy top-level modules
  ([`29f3c95`](https://github.com/CharlesW1/Python-Image-Clicker/commit/29f3c95bb78d7784bc4917a9d851cde116afc9cc))

Move implementation into the src/clicker package; remove duplicate top-level modules
  (clicker_config.py, clicker_logging.py, clicker_killswitch.py, clicker_imaging.py,
  clicker_window.py).
