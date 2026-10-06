# Calendar Grid

Calendar Grid is a LaTeX3 package for deterministic, presentation-neutral month and year grids. It computes proleptic Gregorian dates with integer arithmetic, so the same date calculations are used by pdfLaTeX, XeLaTeX, and LuaLaTeX.

## Features

- Fixed six-week or compact month grids, with any of the seven weekdays as the first column.
- Adjacent-month dates or empty overflow cells.
- Twelve-month year overviews with one to four columns.
- Per-date notes and named, inclusive date ranges, including ranges crossing month and year boundaries.
- Configurable month and weekday labels, cell dimensions, and formatting hooks.
- No graphics package, external font, shell escape, network access, or external program is needed.

## Quick example

```latex
\documentclass{article}
\usepackage{calendar-grid}

\begin{document}
\CalendarGrid[
  year=2027,
  month=1,
  week-start=monday,
  layout=fixed,
  overflow=adjacent
]
\end{document}
```

Register notes and inclusive ranges before the grid command:

```latex
\CalendarGridEvent{2027-01-15}{Project review}
\CalendarGridRange[style=sprint]{2027-01-11}{2027-01-22}
\CalendarGrid[year=2027,month=1]
```

The `\CalendarGridFormatDay` hook receives the ISO date, day number, whether the date belongs to the requested month, weekday number (Monday = 1), weekend flag, row, column, event text, and a comma-separated list of active range style names. The default marks current-month weekend and range dates in bold, prints event text in a small size, and prints adjacent dates in italics. Redefine the hook to apply a document-specific visual style.

## Installation

Copy `calendar-grid.sty` to a directory searched by TeX, or install the package through a TeX distribution when it becomes available there. The package depends only on the standard `array` package.

## Documentation

See [`calendar-grid-doc.pdf`](calendar-grid-doc.pdf) for the user guide and [`calendar-grid-doc.tex`](calendar-grid-doc.tex) for its source. Runnable examples are named `calendar-grid-example-*.tex`.

## Compatibility

The package targets LaTeX formats dated 2020-10-01 or later and is designed for pdfLaTeX, XeLaTeX, and LuaLaTeX. Date inputs use the exact `YYYY-MM-DD` form and Gregorian civil years 0001 through 9999. ISO week numbers are intentionally not included in version 1.0.0.

## Development

Run `l3build check` for regression tests and `l3build doc` to build the guide. The test configuration covers pdfTeX, XeTeX, and LuaTeX. See `CHANGELOG.md` for implemented release contents.

## License

Copyright (C) 2026 Mateo Pedersen. This work may be distributed and/or modified under the conditions of the LaTeX Project Public License, version 1.3c or (at your option) any later version. The license is available at <https://www.latex-project.org/lppl/lppl-1-3c.txt>. LPPL maintenance status: maintained. The current maintainer is Mateo Pedersen.

## Maintainer

Mateo Pedersen, Beta Calendars. Package issues and support are handled through the [GitHub issue tracker](https://github.com/mateopedersen/calendar-grid-latex/issues).

## Project

Calendar Grid is maintained as part of the Beta Calendars developer tooling project. See [Beta Calendars](https://www.betacalendars.com/).
