# AutoDOC container image: install the built wheel and expose the CLI.
# Build the wheel first (make package), then:
#   docker build -t autodoc .
#   docker run --rm -v "$PWD:/workspace" -w /workspace autodoc check --repo /workspace
FROM python:3.11-slim

COPY dist/autodoc_docs-*-py3-none-any.whl /tmp/
RUN python -m pip install --no-cache-dir /tmp/autodoc_docs-*-py3-none-any.whl \
    && rm -f /tmp/autodoc_docs-*.whl

ENTRYPOINT ["autodoc"]
CMD ["--help"]
