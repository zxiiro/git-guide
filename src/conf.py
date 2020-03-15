import sphinx_rtd_theme

project = 'Git - a follow along guide'
copyright = '2020, Thanh Ha'
author = 'Thanh Ha'

extensions = [
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.todo",
    "sphinx_rtd_theme",
]

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'canonical_url': 'https://www.zxiiro.ca/git-guide',
    'analytics_id': 'UA-46385504-1',
    'logo_only': False,
    'display_version': False,
    'prev_next_buttons_location': 'both',
    'style_external_links': False,
    # Toc options
    'collapse_navigation': False,
    'sticky_navigation': True,
    'navigation_depth': 2,
    'includehidden': True,
    'titles_only': False
}
