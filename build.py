import os
import shutil
import subprocess

from bs4 import BeautifulSoup

html_template_path = 'templates/tufte.html'
pandoc_args = ['--standalone', '--smart']

def fix_code_listings(soup):
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

def postprocess_html_file(path):
	soup = BeautifulSoup(open(path, 'r'), 'html.parser')
	fix_code_listings(soup)
	fix_blockquotes_with_citations(soup)

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
