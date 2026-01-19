module.exports = {
  branches: [
    'main',
    { name: 'next', prerelease: true },
    { name: 'beta', prerelease: true },
  ],
  repositoryUrl: 'https://github.com/relaywarden/relaywarden-python-sdk',
  tagFormat: 'v${version}',
  plugins: [
    '@semantic-release/commit-analyzer',
    '@semantic-release/release-notes-generator',
    [
      '@semantic-release/changelog',
      {
        changelogFile: 'CHANGELOG.md',
      },
    ],
    [
      '@semantic-release/exec',
      {
        prepareCmd: 'node -e "const fs=require(\'fs\');const toml=fs.readFileSync(\'pyproject.toml\',\'utf8\');const updated=toml.replace(/^version = \\"[^\\"]+\\"/m,\'version = \\"${nextRelease.version}\\"\');fs.writeFileSync(\'pyproject.toml\',updated)"',
        publishCmd: 'python -m build',
      },
    ],
    [
      '@semantic-release/github',
      {
        assets: [
          { path: 'CHANGELOG.md', label: 'Changelog' },
        ],
      },
    ],
    [
      '@semantic-release/git',
      {
        assets: ['CHANGELOG.md', 'pyproject.toml'],
        message: 'chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}',
      },
    ],
  ],
};
