#let project(title: "", authors: (), date: none, body) = {
  set document(author: authors.map(a => a.name), title: title)
  set page(
    margin: (left: 20mm, right: 20mm, top: 25mm, bottom: 25mm),
    numbering: "1",
    number-align: end,
  )
  set text(font: "Libertinus Serif", lang: "fr", size: 10pt)
  set heading(numbering: "I.1.a.i.")

  // Title row.
  align(center)[
    #block(smallcaps(text(weight: 700, 1.75em, title)))
    #v(1em, weak: true)
    #date
  ]

  // Author information.
  pad(
    top: 0.75em,
    x: 2em,
    grid(
      columns: (1fr,) * calc.min(3, authors.len()),
      gutter: 1em,
      ..authors.map(author => align(center)[
        *#author.name* \
        _#author.email _\
        #smallcaps[#author.affiliation]
      ]),
    ),
  )

  // headings.
  show heading: it => {
    if it.level == 1 {
      v(1.2em)
      text(size: 1.2em)[#smallcaps(it)]
      v(0.7em)
    } else if it.level == 2 {
      v(0.7em)
      text(size: 1.1em)[#it]
      v(0.5em)
    } else if it.level == 3 {
      v(0.5em)
      text(size: 1.05em)[#it]
      v(0.2em)
    } else if it.level == 4 {
      pad(left: 1em, [
        #v(0.3em)
        #text(size: 1em)[_#it _]
        #v(0em)
      ])
    } else {
      it
    }
  }

  show table: set par(justify: false)
  show table: set text(hyphenate: true, size: 1em)

  show raw.where(block: false): box.with(fill: luma(240), inset: (x: 3pt), outset: (y: 3pt), radius: 3pt)
  show table: it => {
    scale(88%, reflow: true)[#it]
  }

  // Main body.
  set par(justify: true)
  set text(hyphenate: false)
  set table(
    inset: 1em,
    align: center,
  )

  show raw.where(block: true): it => {
    set text(size: 0.85em)
    align(center)[#block(width: 95%, inset: 0.2em, breakable: false,)[#it]]
  }
  set table(stroke: 0.5pt + rgb("#888888"), inset: 1em)
  set table(
    fill: (_, y) => if y == 0 { rgb("#e4e4e4") },
  )
  show link: underline
  show outline: set text(size: 0.9em)
  set list(indent: 1em, body-indent: 0.5em)
  set enum(indent: 1em, body-indent: 0.5em)

  body
}
