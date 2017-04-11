---
title: Tufte CSS
author: Dave Liepmann
---

<section>

Tufte CSS provides tools to style web articles using the ideas demonstrated by Edward Tufte’s books
and handouts. Tufte’s style is known for its simplicity, extensive use of sidenotes, tight
integration of graphics with text, and carefully chosen typography.

<!-- Here, we use Pandoc's bracketed spans feature instead of writing <span> tags. -->

Tufte CSS was created by [Dave Liepmann][dave_liepmann] and is now an Edward Tufte project. The
original idea was cribbed from [Tufte-[L[a]{.latex-sup}T[e]{.latex-sub}X]{.latex}][tufte_latex] and
[R Markdown’s Tufte Handout format][tufte_handout]. We give hearty thanks to all the people who have
contributed to those projects.

If you see anything that Tufte CSS could improve, we welcome your contribution in the form of an
issue or pull request on the GitHub project: [tufte-css][tufte_css]. Please note the [contribution
guidelines][contributing].

Finally, a reminder about the goal of this project. The web is not print. Webpages are not books.
Therefore, the goal of Tufte CSS is not to say "websites should look like this interpretation of
Tufte’s books" but rather "here are some techniques Tufte developed that we’ve found useful in
print; maybe you can find a way to make them useful on the web". Tufte CSS is merely a sketch of one
way to implement this particular set of ideas. It should be a starting point, not a design goal,
because any project should present their information as best suits their particular circumstances.

[dave_liepmann]: http://www.daveliepmann.com
[tufte_latex]: http://tufte-latex.github.io/tufte-latex/
[tufte_handout]: http://rmarkdown.rstudio.com/tufte_handout_format.html
[tufte_css]: http://github.com/edwardtufte/tufte-css
[contributing]: http://github.com/edwardtufte/tufte-css#contributing

</section>

<section>
## Getting Started

To use Tufte CSS, copy `tufte.css` and the `et-book` directory of font files to your project
directory, then add the following to your HTML document’s `head` block:

	<link rel="stylesheet" href="tufte.css"/>

Now you just have to use the provided CSS rules, and the Tufte CSS conventions described in this
document. For best results, View Source and Inspect Element frequently.

</section>

<section>
## Fundamentals

### Sections and Headings

Organize your document with an `article` element inside your `body` tag. Inside that, use `section`
tags around each logical grouping of text and headings.

Tufte CSS uses `h1` for the document title, `p` with class `subtitle` for the document subtitle,
`h2` for section headings, and `h3` for low-level headings. More specific headings are not
supported. If you feel the urge to reach for a heading of level 4 or greater, consider redesigning
your document:

<!-- Blockquotes with citations are handled by special postprocessing code that looks for
<blockquote> tags followed by <cite> tags. -->

> [It is] notable that the Feynman lectures (3 volumes) write about all of physics in 1800 pages,
using only 2 levels of hierarchical headings: chapters and A-level heads in the text. It also uses
the methodology of *sentences* which then cumulate sequentially into *paragraphs*, rather than the
grunts of bullet points. Undergraduate Caltech physics is very complicated material, but it didn’t
require an elaborate hierarchy to organize.
<cite>[Edward Tufte, forum post, 'Book design: advice and examples' thread][tufte_forum_post]</cite>

As a bonus, this excerpt regarding the use of headings provides an example of block quotes. In Tufte
CSS they are just lightly styled, semantically correct HTML using `blockquote` and `footer`
elements. See page 20 of [The Visual Display of Quantitative Information][vqdi] for an example in
print.

<!-- Pandoc footnotes are converted to tufte-css sidenotes by postprocessing. -->

[In his later books]{.newthought}[^later_books], Tufte starts each section with a bit of vertical
space, a non-indented paragraph, and the first few words of the sentence set in small caps. For this
we use a span with the class `newthought`, as demonstrated at the beginning of this paragraph.
Vertical spacing is accomplished separately through `<section>` tags. Be consistent: though we do so
in this paragraph for the purpose of demonstration, do not alternate use of header elements and the
`newthought` technique. Pick one approach and stick to it.

[^later_books]: [*Beautiful Evidence*][beautiful_evidence]

[tufte_forum_post]: http://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0000hB
[vqdi]: http://www.edwardtufte.com/tufte/books_vdqi
[beautiful_evidence]: http://www.edwardtufte.com/tufte/books_be

### Text

Although paper handouts obviously have a pure white background, the web is better served by the use
of slightly off-white and off-black colors. Tufte CSS uses `#fffff8` and `#111111` because they are
nearly indistinguishable from their ‘pure’ cousins, but dial down the harsh contrast. We stick to
the greyscale for text, reserving color for specific, careful use in figures and images.

In print, Tufte has used the proprietary Monotype Bembo[^bembo] font. A similar effect is achieved
in digital formats with the now open-source [ETBook][et_book], which Tufte CSS supplies with a
`@font-face` reference to a .ttf file. In case ETBook somehow doesn’t work, Tufte CSS shifts
gracefully to other serif fonts like Palatino and Georgia.

Also notice how Tufte CSS includes separate font files for bold (strong) and italic (emphasis),
instead of relying on the browser to mechanically transform the text. This is typographic best
practice.

<!-- Note: simply wrapping the text below in a <span> tag will change the spacing. -->

<p class='sans'>
If you prefer sans-serifs, use the `sans` class. It relies on Gill Sans, Tufte’s sans-serif font of
choice.
</p>

<!-- The empty span with the 'no-number' class removes the numbering from the previous sidenote. -->

Links in Tufte CSS match the body text in color and do not change on mouseover or when clicked. Here
is a [dummy example](#) that goes nowhere. These links are underlined, since this is the most widely
recognized indicator of clickable text.[^blue_text][]{.no-number} However, because most browsers’
default underlining does not clear descenders and is so thick and distracting, the underline effect
is instead achieved using CSS trickery involving background gradients instead of standard
`text-decoration`. Credit goes to Adam Schwartz for that technique.

As always, these design choices are merely one approach that Tufte CSS provides by default. Other
approaches, such as changing color on click or mouseover, or using highlighting or color instead of
underlining to denote links, could also be made to work. The goal is to make sentences readable
without interference from links, as well as to make links immediately identifiable even by casual
web users.

[^bembo]: See Tufte’s comment in the [Tufte book fonts][tufte_book_fonts] thread.
[^blue_text]: Blue text, while also a widely recognizable clickable-text indicator, is crass and
distracting. Luckily, it is also rendered unnecessary by the use of underlining.

[tufte_book_fonts]: http://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0000Vt
[et_book]: https://github.com/edwardtufte/et-book

</section>
