from pathlib import Path

project_root_dir = Path(__file__).parent.joinpath('..').resolve()

assets_dir = project_root_dir.joinpath('assets')
fonts_dir = assets_dir.joinpath('fonts')

www_dir = project_root_dir.joinpath('www')
www_fonts_dir = www_dir.joinpath('fonts')
www_css_dir = www_dir.joinpath('css')

font_styles = [
    'sans',
    'serif',
]

language_flavors = {
    'CN': 'SC',
    'HK': 'HC',
    'TW': 'TC',
    'JP': '',
    'KR': 'K',
}
