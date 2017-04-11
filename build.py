import os
import shutil
import subprocess

from bs4 import BeautifulSoup

html_template_path = 'templates/tufte.html'

global_pandoc_args = ['--standalone', '--smart', '-t', 'html5', '--section-divs']

def fix_h2_subtitles(soup):
	"""
	<h2 class='subtitle'> tags should really be <p class='subtitle'> tags, but we generate the
	former instead of the latter so that Pandoc inserts the section dividers for us. Now that
	this is done, we perform the conversion.
	"""

	for tag in soup.find_all('section', {'class': 'subtitle'}):
		children = list(tag.children)

		for c in children:
			if c.name is None:
				continue

			assert c.name in {'h1', 'h2', 'h3', 'h4', 'h5', 'h6'}
			c.name = 'p'
			c['class'] = 'subtitle'
			c.extract()

			tag.insert_before(c)
			tag['class'].remove('subtitle')
			return

def fix_code_listings(soup):
	"""
	Pandoc converts code listings to <pre><code> blocks, whereas tufte-css expects
	<pre class='code'>. This functions converts the former to the latter.
	"""

	def is_code_listing_tag(tag):
		if tag.name != 'pre':
			return False

		c = list(tag.children)
		return len(c) == 1 and c[0].name == 'code'

	for tag in soup.find_all(is_code_listing_tag):
		for c in tag.children:
			code = c.contents[0]
			c.decompose()

		tag['class'] = 'code'
		tag.string = code

def fix_citations(soup):
	"""
	Converts <span class='cite'> to <cite>.
	"""

	for tag in soup.find_all('span', {'class': 'cite'}):
		tag.name = 'cite'
		del tag['class']

def fix_blockquotes_with_footers(soup):
	"""
	Puts blockquotes with footers in the format expected by tufte-css.
	"""

	def find_footer(tag):
		for child in reversed(list(tag.children)):
			if child.name is None:
				continue
			if child.name != 'span' or child['class'][0] != 'footer':
				return None

			return child

		return None

	def find_last_p(tag):
		for child in reversed(list(tag.children)):
			if child.name is None:
				continue
			elif child.name != 'p':
				return None

			return child

		return None

	def is_blockquote_with_footer(tag):
		if tag.name != 'blockquote':
			return False

		last_p = find_last_p(tag)
		if last_p is None: return None
		return find_footer(last_p) is not None

	def find_anchor(tag):
		children = list(tag.children)
		child_count = sum([1 for c in children if c.name is not None])
		if child_count != 1: return None

		for c in children:
			if c.name == 'a':
				return c

		return None

	for tag in soup.find_all(is_blockquote_with_footer):
		last_p = find_last_p(tag)
		footer = find_footer(last_p)

		footer.name = 'footer'
		del footer['class']
		tag.append(footer)

		a = find_anchor(footer)
		if a is not None: tag['cite'] = a['href']

def convert_footnotes_to_sidenotes(soup):
	footnotes_tag = soup.find('section', {'class': 'footnotes'})
	footnotes_tag.extract()

	def footnote_content(tag):
		"""
		After each footnote, Pandoc inserts a small anchor with a backarrow symbol that
		directs the browser back to the citation. 
		"""

		children = list(tag.children)
		assert len(children) > 0
		assert children[-1].name == 'a'
		return children[:-1]

	footnotes = []
	counter = 1

	for tag in footnotes_tag.ol.children:
		if tag.name != 'li':
			continue

		children = list(tag.children)
		assert len(children) == 1
		content = footnote_content(children[0])

		assert int(tag['id'][2:]) == counter
		footnotes.append(content)
		counter += 1

	for index, content in enumerate(footnotes):
		s = str(index + 1)
		a = soup.find('a', {'class': 'footnoteRef', 'href': '#fn' + s, 'id': 'fnref' + s})

		n = a.next_sibling

		if n is not None and n.name == 'span' and n['class'][0] == 'unnumbered':
			use_number = False
		else:
			use_number = True

		new_id = 'sidenote-' + s

		label = soup.new_tag('label')
		label['for'] = new_id

		if use_number:
			label['class'] = 'margin-toggle sidenote-number' 
		else:
			label['class'] = 'margin-toggle'
			label.string = '\N{CIRCLED PLUS}'

		input = soup.new_tag('input')
		input['id'] = new_id
		input['type'] = 'checkbox'
		input['class'] = 'margin-toggle'

		span = soup.new_tag('span')
		span['class'] = 'sidenote' if use_number else 'marginnote'

		for tag in content:
			span.append(tag)

		a.insert_after(label)
		label.insert_after(input)
		input.insert_after(span)
		a.decompose()

def postprocess_html_file(path):
	soup = BeautifulSoup(open(path, 'r'), 'html.parser')
	fix_h2_subtitles(soup)
	fix_code_listings(soup)
	fix_citations(soup)
	fix_blockquotes_with_footers(soup)
	convert_footnotes_to_sidenotes(soup)

	with open(path, 'w') as f:
		f.write(str(soup))

shutil.rmtree('output')
os.mkdir('output')

shutil.copytree('css', 'output/css')
shutil.copytree('fonts', 'output/fonts')

os.mkdir('output/posts')

os.mkdir('output/posts/tufte')
shutil.copytree('posts/tufte/images', 'output/posts/tufte/images')

input_path = 'posts/tufte/tufte.md'
output_path = 'output/posts/tufte/tufte.html'

subprocess.run(['pandoc', *global_pandoc_args, '-i', input_path, '-o', output_path,
	'--template=' + html_template_path, '--variable', 'subtitle=Dave Liepmann'])
postprocess_html_file(output_path)
