-- Copyright (C) 2026 Mateo Pedersen.
-- This work is distributed under the LaTeX Project Public License 1.3c or later.
module = "calendar-grid"
bundle = "calendar-grid"
sourcefiles = {"calendar-grid.sty", "build.lua", "scripts/*.py"}
installfiles = {"calendar-grid.sty"}
typesetfiles = {"calendar-grid-doc.tex"}
typesetsourcefiles = {"calendar-grid.sty"}
demofiles = {"calendar-grid-example-*.tex"}
docfiles = {"testfiles/*.lvt", "testfiles/*.tlg"}
textfiles = {"README.md", "LICENSE", "CHANGELOG.md", "manifest.txt"}
testfiledir = "."
checkengines = {"pdftex", "xetex", "luatex"}
stdengine = "pdftex"
checkruns = 1
checksearch = true
typesetexe = "xelatex"
typesetopts = "-interaction=nonstopmode -halt-on-error -file-line-error"
ctanpkg = "calendar-grid"
ctanreadme = "README.md"
ctanzip = "calendar-grid-1.0.0"
excludefiles = {"*~", "config-*.lua"}
uploadconfig = {
  pkg = "calendar-grid",
  version = "1.0.0",
  author = "Mateo Pedersen",
  license = "lppl1.3c",
  summary = "Deterministic month and year calendar grids for LaTeX",
  description = "A LaTeX3 package for deterministic Gregorian month and year grids with configurable week starts, fixed or compact layouts, overflow dates, annotations, and ranges.",
  announcement = "Calendar Grid is a LaTeX3 package for deterministic month and year calendar grids. It provides configurable week starts, fixed or compact layouts, optional adjacent-month dates, event notes, inclusive named ranges, and reusable formatting hooks.",
  ctanPath = "/macros/latex/contrib/calendar-grid",
  repository = "https://github.com/mateopedersen/calendar-grid-latex",
  home = "https://github.com/mateopedersen/calendar-grid-latex",
  bugtracker = "https://github.com/mateopedersen/calendar-grid-latex/issues",
  support = "https://github.com/mateopedersen/calendar-grid-latex/issues",
  development = "https://github.com/mateopedersen/calendar-grid-latex",
  topic = {"Calendar", "Macro support"},
  update = false,
}
