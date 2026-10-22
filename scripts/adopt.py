#!/usr/bin/env python3
"""Read-only scan of an existing project to suggest applicable AutoDOC domains."""
import argparse
import os
from pathlib import Path

# Adoption hints should be fast and should not crawl virtual environments, package caches or
# build outputs. These exclusions affect only this read-only heuristic scan.
SKIP_DIRS = frozenset({
    '.git', '.hg', '.svn', '.venv', 'venv', 'env', 'node_modules',
    '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.tox', '.nox',
    '.next', '.nuxt', '.turbo', '.cache', 'build', 'dist', 'target',
})

RULES = [
    ('API contracts', ('openapi.yaml', 'routes.json', 'package.json'), 'A08-APIS'),
    ('Data', ('schema.sql', 'schema.prisma', 'models.py'), 'A05-DATA'),
    ('Build and supply chain', ('pyproject.toml', 'package-lock.json', 'Cargo.toml', 'go.mod'), 'A10-BUILD'),
    ('AI/ML', ('model.py', 'prompts', 'evals'), 'A21-AI-ML'),
    ('Deployment', ('Dockerfile', 'terraform', 'k8s'), 'A15-RELEASE'),
]


def scan(project):
    # Search only within the selected directory; no writes, imports or code execution. Prune
    # common dependency/build caches before descent so an adoption hint stays bounded in practice.
    names = set()
    for directory, subdirectories, filenames in os.walk(project, followlinks=False):
        subdirectories[:] = [name for name in subdirectories if name not in SKIP_DIRS]
        names.update(subdirectories)
        names.update(filenames)
    return [(name, domain, [signal for signal in signals if signal in names])
            for name, signals, domain in RULES if any(signal in names for signal in signals)]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project-path', required=True, type=Path)
    args = parser.parse_args()
    if not args.project_path.is_dir():
        parser.error('--project-path must be a directory')
    print('Suggested catalog domains (heuristics only; review applicability manually):')
    for name, domain, matches in scan(args.project_path):
        print(f'- {domain} ({name}): {", ".join(matches)}')
    print('Always consider A06-SECURITY, A07-PRIVACY and A11-TESTING; absence of a filename is not proof of non-applicability.')


if __name__ == '__main__':
    main()
