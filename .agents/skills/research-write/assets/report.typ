#let research-report(title: "Reduction research manuscript", date: "", status: "Awaiting expert review", body) = {
  set document(title: title)
  set page(paper: "a4", margin: (x: 24mm, y: 22mm), numbering: "1")
  set text(font: "Libertinus Serif", size: 11pt, lang: "en")
  set par(justify: true, leading: 0.55em)
  set heading(numbering: "1.")
  show figure.caption: set text(size: 9.5pt)
  show figure.caption: it => align(left, it)
  show heading.where(level: 1): set text(size: 13pt)
  show heading.where(level: 2): set text(size: 12pt)
  show raw.where(block: true): block.with(fill: luma(96%), inset: 10pt, width: 100%)
  align(center)[
    #text(size: 18pt, weight: "bold", title)
    #v(8pt)
    #text(size: 10pt, status)
    #if date != "" [#linebreak()#date]
  ]
  v(18pt)
  body
}
