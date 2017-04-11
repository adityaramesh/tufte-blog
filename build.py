import os
import shutil
import subprocess

from bs4 import BeautifulSoup

html_template_path = 'templates/tufte.html'
pandoc_args = ['--standalone', '--smart']

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

def fix_blockquotes_with_citations(soup):
	"""
	Puts blockquotes with citations in the format expected by tufte-css.
	"""

	def find_last_p_with_citation(tag):
		for c in reversed(list(tag.children)):
			if c.name != 'p':
				continue
			
			children = list(c.children)

			if len(children) != 0 and children[-1].name == 'cite':
				return c, children[-1]
			else:
				return None, None

	def is_blockquote_with_citation(tag):
		if tag.name != 'blockquote':
			return False

		return find_last_p_with_citation(tag)[0] is not None

	for tag in soup.find_all(is_blockquote_with_citation):
		last_p, citation = find_last_p_with_citation(tag)

		citation.extract()
		tag['cite'] = citation.a['href']

		citation.name = 'footer'
		tag.append(citation)

def convert_footnotes_to_sidenotes(soup):
	"""
	TODO: support for margin notes (side notes without numbers). Ideally, we should be able to
	support these using 
	"""

	footnotes_tag = soup.find('div', {'class': 'footnotes'})
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

		if n is not None and n.name == 'span' and n['class'][0] == 'no-number':
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
	fix_code_listings(soup)
	fix_blockquotes_with_citations(soup)
	convert_footnotes_to_sidenotes(soup)

	with open(path, 'w') as f:
		f.write(str(soup))

shutil.rmtree('output')
os.mkdir('output')

shutil.copytree('css', 'output/css')
shutil.copytree('fonts', 'output/fonts')
os.mkdir('output/posts')

subprocess.run(['pandoc', *pandoc_args, '-i', 'posts/tufte.md', '-o', 'output/posts/tufte.html',
	'--template=' + html_template_path, '--variable', 'subtitle=Dave Liepmann'])
postprocess_html_file('output/posts/tufte.html')
