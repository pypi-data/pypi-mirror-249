# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [2.0.1] - 2024-01-06

### Added

- Add `py.typed` marker file.

## [2.0.0] - 2024-01-06

### Changed

- Remove class `Tree` and move all methods to `Node`.
- Split `Node` into concrete class `Node` and abstract class `ANode`, for people who don't want to
  use attrs.
- Replace `Node.node_has_data` with `not Node.node_should_prune`.

### Added

- Add powerful depth-first search method `Node.node_visit()`.

## [1.0.0] - 2023-12-24

### Added

- Initial version.
