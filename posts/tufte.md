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

[In his later books<label for="sn-in-his-later-books" class="margin-toggle
sidenote-number"></label></span><input type="checkbox" id="sn-in-his-later-books"
class="margin-toggle"/><span class="sidenote">[*Beautiful
Evidence*][beautiful_evidence]]{.newthought}, Tufte starts each section with a bit of vertical
space, a non-indented paragraph, and the first few words of the sentence set in small caps. For this
we use a span with the class `newthought`, as demonstrated at the beginning of this paragraph.
Vertical spacing is accomplished separately through `<section>` tags. Be consistent: though we do so
in this paragraph for the purpose of demonstration, do not alternate use of header elements and the
`newthought` technique. Pick one approach and stick to it.

[In his later books.^[[*Beautiful Evidence*][beautiful_evidence]]]{.newthought}, Tufte starts each
section with a bit of vertical space, a non-indented paragraph, and the first few words of the
sentence set in small caps. For this we use a span with the class `newthought`, as demonstrated at
the beginning of this paragraph.  Vertical spacing is accomplished separately through `<section>`
tags. Be consistent: though we do so in this paragraph for the purpose of demonstration, do not
alternate use of header elements and the `newthought` technique. Pick one approach and stick to it.

[tufte_forum_post]: http://www.edwardtufte.com/bboard/q-and-a-fetch-msg?msg_id=0000hB
[vqdi]: http://www.edwardtufte.com/tufte/books_vdqi
[beautiful_evidence]: http://www.edwardtufte.com/tufte/books_be

</section>
