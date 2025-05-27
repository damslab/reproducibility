from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np
import sys

if sys.platform.startswith("win"):
    openmp_arg = '-openmp'
    opt_compiler = '/O2'  # Default optimization level for MSVC
else:
    openmp_arg = '-fopenmp'
    opt_compiler = '-O3'  # Default optimization level for GCC

extensions = [
    Extension(
        name="compression.lpc.cameo",
        sources=["compression/lpc/cameo.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="compression.lpc.heap",
        sources=["compression/lpc/heap.pyx"],
        language="c++",
        extra_compile_args=[opt_compiler] 
    ),
    Extension(
        name="compression.lpc.pip",
        sources=["compression/lpc/pip.pyx"],
        language="c++",
        extra_compile_args=[opt_compiler] 
    ),
    Extension(
        name="compression.lpc.pip_heap",
        sources=["compression/lpc/pip_heap.pyx"],
        language="c++",
        extra_compile_args=[opt_compiler] 
    ),
    Extension(
        name="compression.lpc.vw",
        sources=["compression/lpc/vw.pyx"],
        language="c++",
        extra_compile_args=[opt_compiler] 
    ),
    Extension(
        name="compression.lpc.tp",
        sources=["compression/lpc/tp.pyx"],
        language="c++",
        extra_compile_args=[opt_compiler] 
    ),
    Extension(
        name="compression.lpc.inc_acf",
        sources=["compression/lpc/inc_acf.pyx"],
        language="c++",
        extra_compile_args=[opt_compiler] 
    ),
    Extension(
        name="compression.lpc.math_utils",
        sources=["compression/lpc/math_utils.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="compression.lpc.swab",
        sources=["compression/lpc/swab.pyx"],
        language="c++",
        extra_compile_args=[opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="compression.lpc.heap_swab",
        sources=["compression/lpc/heap_swab.pyx"],
        language="c++",
        extra_compile_args=[opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="compression.hpc.hp_agg_cameo",
        sources=["compression/hpc/hp_agg_cameo.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="compression.hpc.hp_heap",
        sources=["compression/hpc/hp_heap.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="compression.hpc.hp_acf_agg_model",
        sources=["compression/hpc/hp_acf_agg_model.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler], 
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="compression.hpc.hp_math_lib",
        sources=["compression/hpc/hp_math_lib.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="compression.hpc.hp_agg_pip",
        sources=["compression/hpc/hp_agg_pip.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="compression.hpc.hp_pip_heap",
        sources=["compression/hpc/hp_pip_heap.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="compression.hpc.hp_agg_tp",
        sources=["compression/hpc/hp_agg_tp.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="compression.hpc.hp_agg_vw",
        sources=["compression/hpc/hp_agg_vw.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="compression.fgc.fg_cameo",
        sources=["compression/fgc/fg_cameo.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="compression.fgc.fg_agg_cameo",
        sources=["compression/fgc/fg_agg_cameo.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="anomaly_detection.irregular_ts",
        sources=["anomaly_detection/irregular_ts.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
    Extension(
        name="anomaly_detection.irregular_mp",
        sources=["anomaly_detection/irregular_mp.pyx"],
        language="c++",
        extra_compile_args=[openmp_arg, opt_compiler],
        extra_link_args=[openmp_arg] if '-f' in openmp_arg else []
    ),
]

setup(
    name='cameo',
    version="0.1",
    packages=["compression"],
    ext_modules=cythonize(extensions, show_all_warnings=True, annotate=True),
    include_dirs=[np.get_include()]
)
