"""Inline SVG icon library for the Chatudo site.

Every icon is stroke-based, 24x24, currentColor, no external requests,
no emoji, no raster images. Used instead of any emoji glyph (rule:
no emoji anywhere in UI, including characters like the check mark,
the multiplication-x or the rightward arrow).
"""

_WRAP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">{}</svg>'

_PATHS = {
    "moon": '<path d="M20.5 14.5A8.5 8.5 0 1 1 9.5 3.5a7 7 0 0 0 11 11Z"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="16" rx="2.5"/><path d="M3.5 9.5h17M8 3v4M16 3v4"/>',
    "chat-stack": '<path d="M4 5.5h13a2 2 0 0 1 2 2V13a2 2 0 0 1-2 2H10l-4 3v-3H6a2 2 0 0 1-2-2V7.5a2 2 0 0 1 2-2Z"/>',
    "pencil": '<path d="M4 20l1-4.2L15.8 5a1.8 1.8 0 0 1 2.5 0l.7.7a1.8 1.8 0 0 1 0 2.5L8.2 19 4 20Z"/><path d="M13.5 6.5l4 4"/>',
    "bell": '<path d="M6 10a6 6 0 1 1 12 0c0 4 1.5 5.3 1.5 5.3H4.5S6 14 6 10Z"/><path d="M10 18.5a2 2 0 0 0 4 0"/>',
    "book": '<path d="M5 4.5h10a3 3 0 0 1 3 3V20l-3-2-3 2-3-2-3 2V7.5a3 3 0 0 1-1-2.3A2.7 2.7 0 0 1 5 4.5Z"/><path d="M5 4.5a2.7 2.7 0 0 0 0 5.4h10"/>',
    "chart": '<path d="M4 20V10M11 20V4M18 20v-7"/><path d="M3 20.5h18"/>',
    "link": '<path d="M9.5 14.5l5-5"/><path d="M8 16l-2 2a3.4 3.4 0 0 1-4.8-4.8l3-3A3.4 3.4 0 0 1 9 8"/><path d="M16 8l2-2a3.4 3.4 0 1 1 4.8 4.8l-3 3a3.4 3.4 0 0 1-4.8 0"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19.5 7"/>',
    "cap": '<path d="M2.5 9.5L12 5l9.5 4.5L12 14 2.5 9.5Z"/><path d="M6.5 11.5v4.2c0 1.3 2.5 2.8 5.5 2.8s5.5-1.5 5.5-2.8v-4.2"/>',
    "bag": '<path d="M6.5 8h11l1 12.5h-13Z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/>',
    "sparkle": '<path d="M12 3.5l1.7 4.8 4.8 1.7-4.8 1.7-1.7 4.8-1.7-4.8-4.8-1.7 4.8-1.7Z"/><path d="M19 15.5l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8Z"/>',
    "shield": '<path d="M12 3l7 3v5.5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6Z"/><path d="M9 12l2 2 4-4.2"/>',
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="2.2"/><path d="M4 7l8 6 8-6"/>',
    "phone": '<path d="M6 3.5h3l1.5 4-2 1.7a12 12 0 0 0 5.3 5.3l1.7-2 4 1.5v3a2 2 0 0 1-2.2 2A17 17 0 0 1 4 6.7 2 2 0 0 1 6 3.5Z"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "arrow-right": '<path d="M4.5 12h15M13.5 6l6 6-6 6"/>',
    "info": '<circle cx="12" cy="12" r="8.5"/><path d="M12 11v5.5"/><circle cx="12" cy="8" r="0.9" fill="currentColor" stroke="none"/>',
    "map-pin": '<path d="M12 21s7-6.4 7-12a7 7 0 1 0-14 0c0 5.6 7 12 7 12Z"/><circle cx="12" cy="9" r="2.3"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3.2 2"/>',
    "users": '<circle cx="9" cy="9" r="3.2"/><path d="M3.2 19c0-3.2 2.6-5.5 5.8-5.5S14.8 15.8 14.8 19"/><circle cx="17" cy="9.5" r="2.6"/><path d="M16 13.6c2.6.2 4.5 2.2 4.8 5"/>',
}


def icon(name: str) -> str:
    path = _PATHS.get(name)
    if path is None:
        raise KeyError(f"unknown icon: {name}")
    return _WRAP.format(path)
