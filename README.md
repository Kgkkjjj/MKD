# MKD

MKD is a lightweight package manager prototype written in C. It wraps common
`pacman` and AUR helper (`yay`) commands behind a simple interface.

## Features

- Install packages from the official repositories or AUR via `yay`
- Remove installed packages
- Search for packages
- Update package databases

## Building

```
make
```

This will produce an executable named `mkd`.

## Usage

```
./mkd <command> [args]
```

Available commands:

- `install <pkg>` – install a package using `yay`
- `remove <pkg>` – remove a package via `pacman`
- `search <query>` – search for packages
- `update` – update package databases
- `fallbacks` – list fallback package systems if AUR or `yay` fail

This project is a minimal example and does not yet implement full dependency
resolution or repository management.

### Fallback Package Systems

If `yay` encounters errors, MKD will display a list of alternative package
systems you can try. The current list includes:

1. apt
2. dnf
3. yum
4. zypper
5. portage
6. pkg
7. homebrew
8. chocolatey
9. snap
10. flatpak
11. pip
12. npm
13. cargo
