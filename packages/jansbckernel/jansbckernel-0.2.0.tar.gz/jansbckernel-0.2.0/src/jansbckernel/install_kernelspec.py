#!/usr/bin/env python
# *_* coding: utf-8 *_*

"""Kernel installer"""

import os
import shutil
from jupyter_client.kernelspec import KernelSpecManager

JSON ="""{"argv":["python","-m","jansbckernel", "-f", "{connection_file}"],
 "display_name":"bc"
}"""

SVG = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with Inkscape (http://www.inkscape.org/) -->

<svg
   version="1.1"
   id="svg2"
   width="337"
   height="337"
   viewBox="0 0 337 337"
   xmlns="http://www.w3.org/2000/svg"
   xmlns:svg="http://www.w3.org/2000/svg">
  <defs
     id="defs6" />
  <g
     id="g8">
    <g
       id="g3591"
       transform="matrix(1.0830189,0,0,1.0830189,26.541547,-11.438562)">
      <rect
         style="opacity:1;fill:#eac435;fill-opacity:1;stroke-width:2.96754;stroke-miterlimit:7"
         id="rect1770"
         width="231.10878"
         height="304.69565"
         x="15.522231"
         y="13.797539"
         ry="26.445282" />
      <rect
         style="opacity:1;fill:#000000;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="rect1774"
         width="165.57047"
         height="68.412796"
         x="49.441177"
         y="39.093025"
         ry="15.522231" />
      <rect
         style="opacity:1;fill:#000000;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="rect2088"
         width="11.497949"
         height="113.82969"
         x="26.445282"
         y="45.416897"
         ry="5.7489743" />
      <rect
         style="opacity:1;fill:#000000;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="rect2090"
         width="76.461357"
         height="74.736664"
         x="137.97539"
         y="121.87826"
         ry="17.821815" />
      <rect
         style="opacity:1;fill:#000000;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="rect2090-2"
         width="76.461357"
         height="74.736664"
         x="49.153736"
         y="121.87826"
         ry="17.821815" />
      <rect
         style="opacity:1;fill:#000000;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="rect2090-0"
         width="76.461357"
         height="74.736664"
         x="49.153736"
         y="217.31123"
         ry="17.821815" />
      <rect
         style="opacity:1;fill:#000000;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="rect2090-9"
         width="76.461357"
         height="74.736664"
         x="137.97539"
         y="217.31123"
         ry="17.821815" />
      <rect
         style="opacity:1;fill:#eac435;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="rect3520"
         width="10.923051"
         height="39.667923"
         x="81.635437"
         y="140.99361"
         ry="5.4615254" />
      <rect
         style="opacity:1;fill:#eac435;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="rect3522"
         width="39.093025"
         height="10.491879"
         x="68.125343"
         y="155.94093"
         ry="5.2459393" />
      <rect
         style="opacity:1;fill:#eac435;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="rect3524"
         width="40.386543"
         height="11.2105"
         x="157.37817"
         y="155.22231"
         ry="5.2459393" />
      <rect
         style="opacity:1;fill:#eac435;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="rect3526"
         width="37.399277"
         height="10.569361"
         x="222.90102"
         y="113.28793"
         ry="5.2459393"
         transform="rotate(45)" />
      <rect
         style="opacity:1;fill:#eac435;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="rect3526-0"
         width="37.399277"
         height="10.569361"
         x="99.58551"
         y="-246.88531"
         ry="5.2459393"
         transform="rotate(135)" />
      <rect
         style="opacity:1;fill:#eac435;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="rect3550"
         width="39.955372"
         height="11.2105"
         x="157.66562"
         y="248.78687"
         ry="5.2459393" />
      <circle
         style="opacity:1;fill:#eac435;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="path3552"
         cx="177.71516"
         cy="233.04906"
         r="6.5394583" />
      <circle
         style="opacity:1;fill:#eac435;fill-opacity:1;stroke-width:2.988;stroke-miterlimit:7"
         id="path3552-5"
         cx="177.49957"
         cy="275.08841"
         r="6.5394583" />
    </g>
  </g>
</svg>
"""

def install_kernelspec():
    """create tmp dir and files and installs kernel"""
    kerneldir = "/tmp/jansbckernel/"
    print('Creating tmp files...', end="")
    os.mkdir(kerneldir)

    with open(kerneldir + "kernel.json", "w", encoding="UTF-8") as file:
        file.write(JSON)

    with open(kerneldir + "logo-svg.svg", "w", encoding="UTF-8") as file:
        file.write(SVG)

    print(' Done!')
    print('Installing Jupyter kernel...', end="")

    ksm = KernelSpecManager()
    ksm.install_kernel_spec(kerneldir, 'jansbckernel', user=os.getenv('USER'))

    print(' Done!')
    print('Cleaning up tmp files...', end="")

    shutil.rmtree(kerneldir)

    print(' Done!')
    print('For uninstall use: jupyter kernelspec uninstall jansbckernel')
