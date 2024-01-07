# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
The rules for this file:
  * entries are sorted newest-first.
  * summarize sets of changes - don't reproduce every git log comment here.
  * don't ever delete anything.
  * keep the format consistent:
    * do not use tabs but use spaces for formatting
    * 79 char width
    * YYYY-MM-DD date format (following ISO 8601)
  * accompany each entry with github issue/PR number (Issue #xyz)
-->

## [1.1.0] -- 2024-01-06

### Authors
- IAlibay

### Added
- Added conda-forge install instruction to docs (Issue #13, PR #14)
- Support for Python 3.12 (Issue #11, PR #12)

### Fixed
- Changed logger to no longer point to MDAnalysis.analysis

### Changed
- Switch from versioneer to versioningit

## [1.0.1] -- 2023-10-26

### Authors
- ianmkenney

### Added
- GitHub action workflow for automatic PyPI package deployment (PR #3)

### Fixed
- pyproject.toml explicitly includes all dependencies and no longer relies
  on the MDAnalysis dependency stack (PR #3)

## [1.0.0] -- 2023-10-10

The original `MDAnalysis.analysis.psa` was written by Sean Seyler in 2015
and had been part of MDAnalysis since release 0.10.0,
https://docs.mdanalysis.org/2.6.1/documentation_pages/analysis/psa.html.
Ian Kenney created the `pathsimanalysis` MDAKit in 2023, based on the original
code in MDAnalysis. Additional contributors to the original source code are
listed in the AUTHORS.md file.

### Added

- the core functionality of PathSimAnalysis (and its tests) was implemented
  using the source code from MDAnalysis.analysis.psa
- PRs trigger Read the Docs for debugging documentation (PR #1)
- GitHub actions workflow for building and deploying docs to GitHub pages 
  (PR #2)

[Unreleased]: https://github.com/MDAnalysis/PathSimAnalysis/compare/1.0.1...HEAD
[1.0.1]: https://github.com/MDAnalysis/PathSimAnalysis/compare/1.0.0...1.0.1
[1.0.0]: https://github.com/MDAnalysis/PathSimAnalysis/releases/tag/1.0.0
