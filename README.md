# gh-action-label-to-semver

## Examples

```yml
name: Bump Version
on:
  pull_request:
    types: [closed]

jobs:
  bumpversion:
    runs-on: ubuntu-latest
    if: github.event.pull_request.merged == 'true'
    steps:
      - name: get next version
        id: nextversion
        uses: "fcurella/gh-action-label-to-semver@main"
        with:
          major: "bump-version-major"
          minor: "bump-version-minor"
          defaultPart: "patch"
          githubToken: ${{ secrets.GITHUB_TOKEN }}
```

## Variables

### Inputs

* `githubToken`: Your GitHub token. Required.
* `major` - Comma-separated list of labels triggering a MAJOR version bump. Defaults to `''`.
* `minor` - Comma-separated list of labels triggering a MINOR version bump. Defaults to `''`.
* `patch` - Comma-separated list of labels triggering a PATCH version bump. Defaults to `''`.
* `defaultPart` - SemVer part to fallback to if no labels are matched. Defaults to the
  special value `'null'`.

### Outputs


* `part` - The SemVer part that should be bumped. `'major'`, `'minor'`, `'patch'` or
  `'null'`. If multiple labels are matched, the highest part will be returned. If no labels
  are matched, `inputs.defaultPart` is returned,
