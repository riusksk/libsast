# -*- coding: utf_8 -*-
"""Semantic Grep Helpers."""
import json
import platform
import multiprocessing
from io import StringIO


def invoke_semgrep(paths, scan_rules, **kwargs):
    """Call Semgrep."""
    if platform.system() == 'Windows':
        return None
    from semgrep import semgrep_main, util
    from semgrep.constants import OutputFormat
    from semgrep.output import OutputHandler, OutputSettings
    try:
        cpu_count = multiprocessing.cpu_count()
    except NotImplementedError:
        cpu_count = 1  # CPU count is not implemented on Windows
    util.set_flags(False, True, False)  # Verbose, Quiet, Force_color

    io_capture = StringIO()
    output_handler = OutputHandler(
        OutputSettings(
            output_format=OutputFormat.JSON,
            output_destination=None,
            error_on_findings=False,
            strict=False,
        ),
        stdout=io_capture,
    )
    semgrep_main.main(
        output_handler=output_handler,
        target=[pt.as_posix() for pt in paths],
        jobs=cpu_count,
        pattern=None,
        lang=None,
        config=scan_rules,
        **kwargs,
    )
    output_handler.close()
    return json.loads(io_capture.getvalue())
