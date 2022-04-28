# How DALL·E 2 Works

[^variations][]{-} [DALL·E 2][dalle2] is a system for text-to-image generation developed [by my coauthors and me][paper]
at [OpenAI.][openai] When prompted with a caption, the system will attempt to generate a novel image from scratch that
matches it. It also has additional capabilities like:

  - **Inpainting:** perform edits to an image using language;
  - **Variations (Figure 1):** generate new images that share the same essence as a given reference image, but differ in
    how the details are put together; and
  - **Text diffs (Figure 4):** transform any aspect of an image using language.

[^variations]: ![](posts/dalle2/images/variations.jpg) Figure 1: variations from DALL·E&nbsp;2 on a blackboard doodle by
Lei Pan. The original doodle is in the center, and the generated variations are displayed around it.

The system underlying DALL·E 2, which we call unCLIP, is based on two key technologies: [CLIP][clip] and
[diffusion][diffusion]. As stated in the blog, CLIP is a model that "efficiently learns visual concepts from natural
language supervision". Diffusion is a technique to train a generative model for images by learning to undo the steps of
a fixed corruption process. We briefly describe both of these technologies next.

[^clip_fig][]{-} CLIP consists of two neural networks -- a text encoder and an image encoder -- that are trained on a
large, diverse collection of image-text pairs. Each encoder maps its input to a point on a globe (known as an
_embedding_) that functions as a "concept space" shared by both modalities. During each step of training, CLIP receives
a list of images and a corresponding list of captions that describe them. Using this data, we can form two types of
image-text pairs: a _matching_ pair, in which an image is paired up with its corresponding caption, and a _mismatching_
pair, in which an image is paired up with any other caption. The encoders are trained to map the matching pairs to
nearby points on this globe, and mismatching pairs to distant points.

This simple training objective[^contrastive] encourages CLIP to learn about all of the features of an image that people
are likely to write about online. These features include things like which objects are present, the aesthetic style, the
colors and materials that are used, and so on. By contrast, CLIP is typically _not_ incentivized to preserve information
about the relative positions of objects, or information about which attributes apply to which objects. CLIP would
therefore have a hard time distinguishing between, say, an image of a red cube on top of a blue cube and another image
in which the positions of the two objects are swapped. The reason for this is the nature of the CLIP training objective:
CLIP is only incentivized to learn the features of an image that are sufficient to match it up with the correct caption
(as opposed to any of the others in the list). Unless it receives a counterexample (i.e., a caption that mentions a blue
cube on top of a red cube), CLIP will not learn to preserve information about the objects' relative positions.

[^contrastive]: Known as "contrastive training" in machine learning.

[clip]: https://openai.com/blog/clip/
[diffusion]: https://arxiv.org/abs/2006.11239
[^clip_fig]: ![](posts/dalle2/images/clip.jpg) Figure 2: illustration of the contrastive training objective for CLIP.
During each step of training, CLIP receives $N = 32{,}786$ images and their corresponding captions. From these, we form
$N$ matching image-caption pairs (corresponding to the diagonal elements of the matrix in the illustration), and $N (N -
1)$ pairs of mismatching captions and images (corresponding to the off-diagonal elements).<br/><br/>

[^diffusion_fig][]{-} A diffusion model is trained to undo the steps of a fixed corruption process. Each step of the
corruption process adds a small amount of noise[^noise] to an image, which erases some of the information in it. After
the final step, the image becomes indistinguishable from pure noise. The diffusion model is trained to reverse this
process, and in doing so learns to regenerate what might have been erased in each step. To generate an image from
scratch, we start with pure noise and suppose that it was the end result of the corruption process applied to a real
image. Then, we repeatedly apply the model to reverse each step of this hypothetical corruption process. This gradually
makes the image more and more realistic, eventually yielding a pristine, noiseless image.

[^noise]: Specifically, gaussian noise.
[^diffusion_fig]: ![](posts/dalle2/images/diffusion.gif) Figure 3: illustration of the process used to generate a new
image with the diffusion model, created by [Alex Nichol.][alex]<br/><br/>

DALL·E 2 generates images in a two-stage process, first by generating the "gist" of an image and then by filling in the
remaining details to obtain a realistic image. In the first stage, a model which we call the prior generates the CLIP
image embedding (intended to describe the "gist" of the image) from the given caption.[^why_prior] In the second stage,
a diffusion model which we call unCLIP generates the image itself from this embedding. During each step of training,
unCLIP receives both a corrupted version of the image it is trained to reconstruct, as well as the CLIP image embedding
of the clean image. This model is called unCLIP because it effectively reverses the mapping learned by the CLIP image
encoder. Since unCLIP trained to "fill in the details" necessary to produce a realistic image from the embedding, it
will learn to model all of the information that CLIP deems irrelevant for its training objective and hence discards.

[^why_prior]: One might ask why this prior model is necessary: since the CLIP text encoder is trained to match the
output of the image encoder, why not use the output of the text encoder as the "gist" of the image? The answer is that
an infinite number of images could be consistent with a given caption, so the outputs of the two encoders will not
perfectly coincide. Hence, a separate prior model is needed to "translate" the text embedding into an image embedding
that could plausibly match it.

There's a few reasons why it's advantageous to use this two-stage sampling process, and we discuss two of them
here.[^why_clip] Firstly, we can prioritize modeling the high-level semantics that make images meaningful to humans
above other details. Images contain a lot of information, most of which is used to describe to fine-grained,
imperceptible details. Only a relatively tiny sliver of this information is responsible for what makes images visually
coherent and meaningful to us, and the CLIP image embedding captures much of it. Training a model directly on the CLIP
image embedding allows us to focus on modeling these salient characteristics first, before filling in the details
necessary to synthesize a realistic image in the second stage.

[^why_clip]: [Our paper][paper] discusses further advantages of the two-stage sampling process.

[^house][]{-} The second reason is that CLIP's multimodal embedding space allows us to apply "before and after"
transformations to images using a technique that we call _text diffs_. In 2013, [word2vec][word2vec] showed that it is
possible to obtain a "concept space" for text in which vector arithmetic becomes interpretable. For example, word2vec
maps the word "queen" close to the result of computing
$$
    \textrm{“woman”} + \textrm{“king”} - \textrm{“man”},
$$
which makes it possible to complete analogies of the sort one might encounter in a standardized test. CLIP takes this a
step further and allows us to perform arithmetic using _both_ text and images, as in
$$
    \textrm{(image of victorian house)} + \textrm{“a modern house”} - \textrm{“a victorian house”}.
$$
Using unCLIP, we can translate points in CLIP's concept space back into images and visually inspect the change that is
taking place as we move the embedding of the image in the direction specified by the "before" caption ("a victorian
house") and the "after" caption ("a modern house").[^text_diff_math] The animation shows this trajectory, and provides
us with visual confirmation that the image of a victorian house that we started out with is indeed being "modernized" as
we might intuitively expect. Of course, text diffs are not limited to architecture: the transformation could be any
"before and after" concept that can be expressed in language, which makes this a versatile and powerful tool.

[^house]: ![](posts/dalle2/images/house.gif) Figure 4: animation of text diff used to transform a Victorian house into a
modern one. The transformation is determined by the captions "a victorian house", which describes the architecture of
the house, and "a modern house", which describes how the architecture of the house should be changed.<br/><br/>

[^text_diff_math]: Concretely, let $f_i$ and $f_t$ denote the CLIP image and text encoders, respectively, and suppose
that we have an image of a Victorian house contained in a file `house.png` which we would like to transform into a
modern house. To do this, we first compute
$$
\begin{align}
z_{i0} &= f_i(\texttt{house.png}), \\
z_{t0} &= f_t(\textrm{“a photo of a victorian house”}), \\
z_{t1} &= f_t(\textrm{“a photo of a modern house”}), \quad\textrm{and} \\
z_d &= (z_{t1} - z_{t0}) / \|z_{t1} - z_{t0}\|,
\end{align}
$$
where $z_d$ is known as the _text diff vector._ Next, to transform the house, we rotate between the image embedding
$z_{i0}$ and the text diff vector $z_d$ using $z_{i1} = \operatorname{slerp}(z_{i0}, z_d, \theta)$. Finally, we
synthesize an image from $z_{i1}$ using unCLIP. The animation shows the trajectory as $\theta$ is varied from 0 (which
reconstructs the original image) to 0.50 (which results in a modernized version of the house).

[dalle2]: https://openai.com/dall-e-2
[paper]: https://arxiv.org/abs/2204.06125
[openai]: https://openai.com
[word2vec]: https://arxiv.org/abs/1310.4546
[prafulla]: https://prafulladhariwal.com
[alex]: https://aqnichol.com
[casey]: http://caseychu.io
[mark]: https://twitter.com/markchen90?lang=en
[aravind]: https://twitter.com/AravSrinivas/with_replies
[rewon]: http://www.rewon.org

_Acknowledgments:_ I'd like to thank Lei Pan, [Aravind Srinivas][aravind], [Rewon Child][rewon] and Justin Mao-Jones for
their feedback on this blog. I'd also like to thank to my coauthors [Prafulla Dhariwal][prafulla], [Alex Nichol][alex],
[Casey Chu][casey], and [Mark Chen][mark].
