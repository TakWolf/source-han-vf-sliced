import os
import shutil
from collections import defaultdict
from io import StringIO
from pathlib import Path

import unidata_blocks
from fontTools import subset
from fontTools.ttLib import TTFont

from tools import fonts_dir, www_fonts_dir, www_css_dir, font_styles, language_flavors


def _alphabet_to_text(alphabet: list[int]) -> str:
    return ''.join(chr(code_point) for code_point in sorted(alphabet))


def _alphabet_to_unicode_range(alphabet: list[int]) -> list[str]:
    pairs = []
    code_start = None
    code_end = None
    for code_point in sorted(alphabet):
        if code_start is None:
            assert code_end is None
            code_start = code_point
            code_end = code_point
        elif code_point == code_end + 1:
            code_end = code_point
        else:
            pairs.append((code_start, code_end))
            code_start = code_point
            code_end = code_point
    pairs.append((code_start, code_end))

    unicode_range = []
    for code_start, code_end in pairs:
        if code_start == code_end:
            unicode_range.append(f'U+{code_start:04X}')
        else:
            unicode_range.append(f'U+{code_start:04X}-{code_end:04X}')
    return unicode_range


def _get_slice_alphabets(alphabet: list[int]) -> list[tuple[str, list[int]]]:
    block_alphabets = defaultdict[str, list[int]](list)
    for code_point in alphabet:
        block = unidata_blocks.get_block_by_code_point(code_point)
        block_alphabets[block.name].append(code_point)

    slice_alphabets = []
    for block_name, block_alphabet in block_alphabets.items():
        slice_name = block_name.replace(' ', '-')
        slice_index = 0
        slice_alphabet = []
        for code_point in sorted(block_alphabet):
            if len(slice_alphabet) >= 200:
                slice_alphabets.append((f'{slice_name}-{slice_index}', slice_alphabet))
                slice_index += 1
                slice_alphabet = []
            slice_alphabet.append(code_point)
        slice_alphabets.append((f'{slice_name}-{slice_index}', slice_alphabet))
    return slice_alphabets


def _slice_font(font_path: Path, output_font_path: Path, alphabet: list[int]):
    args = [
        os.fspath(font_path),
        f'--text={_alphabet_to_text(alphabet)}',
        "--layout-features='*'",
        f'--output-file={os.fspath(output_font_path)}',
    ]
    subset.main(args)


def main():
    if www_fonts_dir.exists():
        shutil.rmtree(www_fonts_dir)
    www_fonts_dir.mkdir(parents=True)
    if www_css_dir.exists():
        shutil.rmtree(www_css_dir)
    www_css_dir.mkdir(parents=True)

    index_css = StringIO()

    for font_style in font_styles:
        font_style_css = StringIO()

        for language_flavor, name_flavor in language_flavors.items():
            font_path = fonts_dir.joinpath(font_style, f'SourceHan{font_style.capitalize()}{name_flavor}-VF.otf.woff2')
            slice_alphabets = _get_slice_alphabets(TTFont(font_path).getBestCmap())

            language_flavor_css = StringIO()

            output_font_dir = www_fonts_dir.joinpath(font_style, language_flavor.lower())
            output_font_dir.mkdir(parents=True)
            for slice_name, slice_alphabet in slice_alphabets:
                print(f'{slice_name}: {len(slice_alphabet)}')

                output_font_path = output_font_dir.joinpath(f'SourceHan{font_style.capitalize()}-{language_flavor}-VF-{slice_name}.otf.woff2')
                _slice_font(font_path, output_font_path, slice_alphabet)
                print(f"Make Font: '{output_font_path}'")

                language_flavor_css.write('\n')
                language_flavor_css.write('@font-face {\n')
                language_flavor_css.write(f'    font-family: SourceHan{font_style.capitalize()}-{language_flavor};\n')
                language_flavor_css.write('    font-display:  swap;\n')
                language_flavor_css.write(f'    src: url("../fonts/{font_style}/{language_flavor.lower()}/{output_font_path.name}") format("woff2");\n')
                language_flavor_css.write(f'    unicode-range: {', '.join(_alphabet_to_unicode_range(slice_alphabet))};\n')
                language_flavor_css.write('}\n')

            language_flavor_css_path = www_css_dir.joinpath(f'{font_style}-{language_flavor.lower()}.css')
            language_flavor_css_path.write_text(language_flavor_css.getvalue(), 'utf-8')
            print(f"Make CSS: '{language_flavor_css_path}'")

            font_style_css.write(f'@import "{language_flavor_css_path.name}";\n')

        font_style_css_path = www_css_dir.joinpath(f'{font_style}.css')
        font_style_css_path.write_text(font_style_css.getvalue(), 'utf-8')
        print(f"Make CSS: '{font_style_css_path}'")

        index_css.write(f'@import "{font_style_css_path.name}";\n')

    index_css_path = www_css_dir.joinpath('index.css')
    index_css_path.write_text(index_css.getvalue(), 'utf-8')
    print(f"Make CSS: '{index_css_path}'")


if __name__ == '__main__':
    main()
