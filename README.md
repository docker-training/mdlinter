# Markdown Linter

## Usage

Pull the `mdlint` image from Docker Hub:

  ```bash
  docker image pull training/mdlint:dev
  ```

In the directory that contains the HTML code you want to check, run:

  ```bash
  docker container run -v $(PWD):/raw training/mdlint:dev
  ```
  
## Checks for:

 - newline at the end of all exercises
 - two spaces after single digit step numerals (ie one-dot-space-space, not just single space)
 - 4 space indents
 - no double blank lines inside code blocks
 - code blocks should be surrounded by a blank line before and after
 - code block lines <= 90 char
 - broken URLs in Markdown files
