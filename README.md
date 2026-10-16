# local-redact

Redact common email addresses, phone numbers and selected secret formats from a UTF-8 text file entirely offline.

## Status

Initial prototype, created in October 2026. This is a small,
independent starter project, without claims of production deployment or adoption.

## Installation

Python 3.10+ is required. No third-party Python packages are needed.
Copy this directory, then run commands from inside it.

## Usage

```sh
python3 cli.py examples/contact.txt --output redacted.txt
```

Run `python3 cli.py --help` for options. Reports go to standard output unless an
output file is specified. Input errors return status 2.

## Limitations

Pattern matching is incomplete and can produce false positives. Review output before sharing. Phone detection covers common mainland China and North American formats; it is not a comprehensive privacy scanner.

## Development and contributing

Keep changes narrowly scoped. Include a reproducible example for a bug report.
Use synthetic fixtures rather than personal, proprietary or research data.
Run the project checks from this directory:

```sh
python3 -m unittest discover -s tests -v
```

## License

MIT; see [LICENSE](LICENSE).
