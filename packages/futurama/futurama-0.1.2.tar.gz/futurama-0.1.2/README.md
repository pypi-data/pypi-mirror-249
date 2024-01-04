# futurama

Random Futurama Quotes

[![Build Status](https://drone.decapod.one/api/badges/brethil/futurama/status.svg?ref=refs/heads/main)](https://drone.decapod.one/brethil/futurama)

## Install

```bash
pip install futurama
```

### Usage

Via command-line:

```
futurama
```

as a python module:

```bash
python -m futurama
```

### zsh

Add this to `.zshrc` to get a random quote for each new shell

```zsh
precmd() {
    if [[ -z "${_futurama_called}" ]]; then
        futurama
        export _futurama_called=true
    fi
}
```
