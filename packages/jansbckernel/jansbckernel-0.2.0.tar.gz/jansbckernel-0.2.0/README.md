# jansbckernel

![alt](https://raw.githubusercontent.com/jans-code/jansbckernel/main/jansbckernel/logo-svg.svg)

A very simple and dirty jupyter kernel for [GNU bc](https://www.gnu.org/software/bc/).
This kernel is a work in progress, so far variables and functions do not carry over to later cells.

## Dev Installation

- install bc from your distro's package manager
- download/clone this project
- open shell in project folder and install dev build
- `pip install -e ./`
- then install kernelspec
- `jansbckernel`
- or
- `jupyter kernelspec install --user jansbckernel`

## Uninstall

- `jupyter kernelspec uninstall jansbckernel`
- `pip uninstall jansbckernel`
