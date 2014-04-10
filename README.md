# astronomer

Get info on the users who've starred a given GitHub repository.

## Installation

`pip install astronomer`

## Usage

Before using `astronomer`, you'll need to [generate a Personal API Token](https://github.com/blog/1509-personal-api-tokens). Don't worry, it's easy. Then, it's just a matter of, for example:

```sh
astronomer jsvine/envplus --token [ENTER TOKEN HERE]
```

If you don't provide the `--token` parameter, `astronomer` will ask you to enter it in a password-style prompt.

Note: Because of GitHub's rate limits, `astronomer` currently only works for repositories with [4,760 stars or fewer](https://www.wolframalpha.com/input/?i=5000%3Dfloor%281+%2B+ceil%28%28x%2F20%29%29+%2B+x%29). (Or [99,965 stars or fewer](https://www.wolframalpha.com/input/?i=5000%3Dfloor%281+%2B+ceil%28%28x%2F20%29%29%29) if you're using the `--minimal` option.)

## Options

### --format [tsv, csv, json]

Specifies the format in which `astronomer` outputs the data. Default: `tsv`.

### --outfile [PATH]

Specifies a file to which `astronomer` outputs the data. Default: *stdout*.

### --quiet

Silence logging.
