from typing import Optional, Callable
from tempfile import NamedTemporaryFile
import re
import os

def _get_matcher(line: Optional[str]) -> Callable[[str], bool]:
    if line:
        regex = re.compile(line)
        return lambda x: regex.match(x) is not None
    else:
        return lambda _: False

def insert_text(input_file: str, text: str, before_line: Optional[str], after_line: Optional[str]) -> None:
    text = text+"\n"
    limit = 1
    input_dir = os.path.dirname(input_file)
    out_fd = NamedTemporaryFile(mode='w', dir=input_dir, delete=False)
    old_dst_file = out_fd.name
    match_before, match_after = _get_matcher(before_line), _get_matcher(after_line)
    try:
        with open(input_file, 'r') as in_fd:
            with out_fd:
                for line in in_fd:
                    rs_line = line.rstrip()
                    if limit and match_before(rs_line):
                        out_fd.write(text + line)
                        limit -= 1
                    elif limit and match_after(rs_line):
                        out_fd.write(line + text)
                        limit -= 1
                    else:
                        out_fd.write(line)

                # Append if no before / after
                if limit and before_line is None and after_line is None:
                    out_fd.write(text)

        os.rename(old_dst_file, input_file)
    except:
        os.unlink(old_dst_file)
        raise
