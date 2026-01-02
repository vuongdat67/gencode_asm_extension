# ASM Suggest

VS Code command that sends selected source to a local ASM suggestion daemon and inserts the returned assembly. Defaults to the top suggestion and lets you pick alternatives when available.

## Features

- Command: ASM Suggest: Insert from Daemon (`asm-suggest.insertAsm`).
- Keybinding: `Ctrl+Alt+Y` when an editor is focused.
- Shows a quick pick if the daemon returns multiple candidates; inserts the best suggestion otherwise.

## Requirements

- Local HTTP daemon running at `http://127.0.0.1:9137/infer` that accepts JSON `{ source, similarity, var_map }` and responds with either `{ best, candidates|alternatives }` or an array of suggestions.
- VS Code 1.107.0 or newer.

## Usage

1) Select source text in an editor.
2) Run ASM Suggest: Insert from Daemon (Command Palette) or press `Ctrl+Alt+Y`.
3) Choose an alternative if prompted; the chosen ASM replaces the selection (or inserts at the cursor if the selection is empty).

## Release Notes

See [CHANGELOG](CHANGELOG.md).
