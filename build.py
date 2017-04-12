import os
import shutil
import subprocess
import jinja2

from bs4 import BeautifulSoup
from argparse import ArgumentParser

build_targets = {'dev', 'prod'}

site_definitions = {
	'dev': {'site': {'url': 'file:///Users/aditya/projects/tufte_blog/output'}},
	'prod': {'site': {'url': 'http://adityaramesh.com'}}
}

template_input_path = 'templates/tufte.html'
template_output_path = 'temp/tufte.html'
global_pandoc_args = ['--standalone', '--smart', '-t', 'html5', '--section-divs']

ap = ArgumentParser()
ap.add_argument('--target', type=str, default='dev')

args = ap.parse_args()
assert args.target in build_targets

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

def fix_fullwidth_tables(soup):
	for tag in soup.find_all('table'):
		for n in tag.next_siblings:
			if n.name is not None:
				break

		if n is not None and n.name == 'span' and 'class' in n and \
			n['class'][0] == 'fullwidth':

			n.decompose()

			if 'class' not in tag: tag['class'] = []
			tag['class'].append('fullwidth')
			del tag['style']

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

def denest_singleton_footnotes(soup):
	for figure_tag in soup.find_all('figure'):
		for child in figure_tag.children:
			if child.name == 'p':
				c = list(child.children)
				if len(c) == 0 or len(c) > 2: continue

				b1 = c[0].name == 'a' and 'footnoteRef' in c[0]['class']
				b2 = len(c) == 1
				b3 = len(c) == 2 and c[1].name == 'span' and \
					'unnumbered' in c[1]['class'] 

				if b1 and (b2 or b3):
					for tag in c:
						tag.extract()
						child.insert_before(tag)

					child.decompose()

def convert_footnotes_to_sidenotes(soup):
	footnotes_tag = soup.find('section', {'class': 'footnotes'})
	if footnotes_tag is None: return
	footnotes_tag.extract()

	def process_footer_child(tag):
		if tag.name == 'a' and tag.next_sibling is None:
			return []
		elif tag.name != 'p':
			return [tag]

		children = list(tag.children)
		assert len(children) > 0

		if tag.next_sibling is not None:
			return children
		else:
			assert children[-1].name == 'a'
			return children[:-1]

	footnotes = []
	counter = 1

	for tag in footnotes_tag.ol.children:
		if tag.name != 'li':
			continue

		assert int(tag['id'][2:]) == counter

		content = [process_footer_child(c) for c in tag.children]
		content = [tag for tag_list in content for tag in tag_list]
		footnotes.append(content)
		counter += 1

	for index, content in enumerate(footnotes):
		s = str(index + 1)
		a = soup.find('a', {'class': 'footnoteRef', 'href': '#fn' + s, 'id': 'fnref' + s})

		n = a.next_sibling

		if n is not None and n.name == 'span' and n['class'][0] == 'unnumbered':
			n.decompose()
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
	fix_fullwidth_tables(soup)
	fix_blockquotes_with_footers(soup)

	denest_singleton_footnotes(soup)
	convert_footnotes_to_sidenotes(soup)

	with open(path, 'w') as f:
		f.write(str(soup))

def render_template(path, context):
	path, filename = os.path.split(path)
	return jinja2.Environment(loader=jinja2.FileSystemLoader(path)) \
		.get_template(filename).render(context)

assert not os.path.exists('temp')
shutil.rmtree('output')

os.mkdir('temp')
os.mkdir('output')

with open(template_output_path, 'w') as f:
	f.write(render_template(template_input_path, site_definitions[args.target]))

shutil.copytree('css', 'output/css')
shutil.copytree('fonts', 'output/fonts')

os.mkdir('output/posts')

for post_name in os.listdir('posts'):
	src_dir = os.path.join('posts', post_name)
	dst_dir = os.path.join('output/posts', post_name)

	post_src_path = os.path.join(src_dir, post_name + '.md')
	post_dst_path = os.path.join(dst_dir, post_name + '.html')
	assert os.path.isfile(post_src_path)

	os.mkdir(dst_dir)

	for file in os.listdir(src_dir):
		if os.path.isdir(file):
			input_path = os.path.join(src_dir, file)
			output_path = os.path.join(dst_dir, file)
			shutil.copytree(input_path, output_path)

	subprocess.run(['pandoc', *global_pandoc_args, '-i', post_src_path, '-o', post_dst_path,
		'--template=' + template_output_path])
	postprocess_html_file(post_dst_path)

shutil.rmtree('temp')
