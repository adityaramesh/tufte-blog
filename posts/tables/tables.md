---
title: Tables
author: Aditya Ramesh
---

# Tables

This document shows the four kinds of tables supported by `tufte-blog`. The tables in this document
are adapted from those in the documentation for [Pandoc][pandoc] and [Tufte-Jekyll.][tufte_jekyll]

[pandoc]: http://pandoc.org
[tufte_jekyll]: http://github.com/clayh53/tufte-jekyll

<figure>
[^margin_caption_1][]{-}

-------------------------
Left       Center   Right
--------- -------- ------
Aardvarks    1      $3.50

Cats         5      $4.23

Dogs         3      $5.29
-------------------------
</figure>

[^margin_caption_1]: This is an example of a normal table. It is capable of stretching to take up
the entirety of the text width in order to accommodate its contents.

<figure>
[^margin_caption_2][]{-}

-------------------------------------------------
                    mpg  cyl  disp  hp  drat   wt
------------------ ---- ---- ----- --- ----- ----
Mazda RX4            21    6   160 110  3.90 2.62

Mazda RX4 Wag        21    6   160 110  3.90 2.88

Datsun 710         22.8    4   108  93  3.85 2.32

Hornet 4 Drive     21.4    6   258 110  3.08 3.21

Hornet Sportabout  18.7    8   360 175  3.15 3.44

Valiant            18.1    6   160 105  2.76 3.46
-------------------------------------------------
[]{.fullwidth}
</figure>

[^margin_caption_2]: This is an example of a table that is forced to take up the entirety of the
text width.

<figure class="fullwidth">
[]{#large-table}

----------------------------------------------------------------------------------------------
Content and tone of front-page articles in 94     Number of  Percent of articles with negative
U.S. newspapers, October and November, 1974        articles    criticism of specific person or
                                                                                        policy
------------------------------------------------ ---------- ----------------------------------
Watergate: defendants and prosecutors, Ford's           537                                49%
pardon of Nixon

Inflation, high cost of living                          415                                28%

Government competence: costs, quality, salaries         322                                30%
of public employees

Confidence in government: power of special              266                                52%
interests, trust in political leaders,
dishonesty in politics

Government power: regulation of business,               154                                42%
secrecy, control of CIA and FBI

Crime                                                   123                                30%

Race                                                    103                                25%

Unemployment                                            100                                13%

Shortages: energy, food                                  68                                16%
----------------------------------------------------------------------------------------------

Table: This is an example of a table that is forced to take up the entirety of the page width.
</figure>

<figure>
[^margin_caption_3][]{-}

+---------------+---------------+--------------------+
| Fruit         | Price         | Advantages         |
+:==============+:==============+:===================+
| Bananas       | $1.34         | - built-in wrapper |
|               |               | - bright color     |
+---------------+---------------+--------------------+
| Oranges       | $2.10         | - cures scurvy     |
|               |               | - tasty            |
+---------------+---------------+--------------------+

</figure>

[^margin_caption_3]: This table was created using Pandoc's grid table syntax. It can contain
arbitrary block elements, such as paragraphs, code blocks, lists, etc. **However, it is not
compatible with the `fullwidth` class.** Neither the table nor its enclosing figure should be
assigned the `fullwidth` class.

## Unsupported Features

Tables like the following currently cannot be created without using raw HTML. This is because Pandoc
[does not yet support the `rowspan` and `colspan` attributes.][pandoc_rowspan_colspan]

<figure>
<table>
<thead>
<tr><th colspan="2" class="cmid">Items</th><th class="no-hrule"></th></tr>
<tr><th style="text-align: left">Animal</th><th style="text-align: left">Description</th><th style="text-align: right">Price ($)</th></tr>
</thead>
<tbody>
<tr><td>Gnat</td><td>per gram</td><td style="text-align: right">13.65</td></tr>
<tr><td></td><td>each</td><td style="text-align: right">0.01</td></tr>
<tr><td>Gnu</td><td>stuffed</td><td style="text-align: right">92.50</td></tr>
<tr><td>Emu</td><td>stuffed</td><td style="text-align: right">33.33</td></tr>
<tr><td>Armadillo</td><td>frozen</td><td style="text-align: right">8.99</td></tr>
</tbody>
</table>
</figure>

[pandoc_rowspan_colspan]: https://github.com/jgm/pandoc/issues/3274

In the future, it may be useful to allow the user to optionally specify a minimum width for each
column of a table. Large tables like [this one][large_table] don't look very good on small screens.
One potential solution would be to scale the font size and line width according to the screen
resolution and DPI. Experience leads me to believe this solution is currently unviable for the
following reasons: (1) it's seldom possible to obtain the true DPI; (2) it's very difficult to
fluidly vary the font size, line height, margins and paddings, etc., so that the page looks good
across a diverse set of displays; and (3), there is a minimum font size beyond which the text
becomes illegible, so each table column should ideally have a minimum width anyway.

[large_table]: output/posts/tables/tables.html#large-table
