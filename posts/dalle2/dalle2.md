# How DALL·E 2 Works

[DALL·E 2][dalle2] is a system for text-to-image generation developed [by me and my coauthors][paper] at
[OpenAI.][openai] Given a caption, the system will attempt to generate a novel image from scratch, pixel-by-pixel, that
matches the caption. It also has additional capabilities called inpainting, variations, and text diffs, which we discuss
in [our paper][paper].

[^clip_fig][]{-} The system underlying DALL·E 2, which we call unCLIP, is based on two key technologies: [CLIP][clip]
and [diffusion][diffusion]. As stated in the blog, CLIP is a model that "efficiently learns visual concepts from natural
language supervision". It is trained on a large, diverse collection of image-text pairs, and consists of two neural
networks: an image encoder and a text encoder. Each encoder maps its input to a 1,024-dimensional _embedding_ in an
abstract concept space that is shared between both modalities. During each step of training, CLIP receives 32,768 images
and their corresponding captions. The encoders are trained to match the embedding of each image with the embedding of
its corresponding caption.

This simple training objective encourages CLIP to learn about all of the features of an image that people are likely to
write about online. These features include things like which objects are present, the aesthetic style, the colors and
materials that are used, and so on. By contrast, CLIP is typically _not_ incentivized to preserve information about the
relative positions of objects, or information about which attributes apply to which objects. This means that CLIP would
have a hard time distinguishing between, say, an image of a red cube on top of a blue cube and another image in which
the positions of the two objects are reversed. The reason for this is the contrastive nature of the CLIP training
objective: CLIP is only incentivized to learn the features of an image that are sufficient to match it up with the
correct caption (out of the other 32,767 for the current training step). Unless it receives a counterexample (i.e., a
caption that mentions a blue cube on top of a red cube), CLIP will not learn to preserve information about the objects'
relative positions.

[clip]: https://openai.com/blog/clip/
[diffusion]: https://arxiv.org/abs/2006.11239
[^clip_fig]: ![](posts/dalle2/images/clip.png) Illustration of the contrastive
training objective for CLIP.

[^diffusion_fig][]{-} Diffusion is a technique to train a generative model for images by learning to undo the steps of a
fixed corruption process. Each step of the corruption process adds a small amount of gaussian noise to the image, which
effectively removes some of the information in it. After the final step, the image becomes indistinguishable from pure
noise. The diffusion model is trained to reverse each step of this process, and in doing so learns to put back
information into the image that did not previously exist. To generate an image, we start with pure noise and repeatedly
apply the model.  This gradually makes the image more and more realistic, with the end result being a pristene,
noiseless image.

[^diffusion_fig]: ![](posts/dalle2/images/diffusion.gif) Illustration of the
process used to generate a new image with the diffusion model, created by coauthor [Alex Nichol.][alex]

DALL·E 2 generates images in a two-stage process. In the first stage, a model which we call the prior generates the CLIP
image embedding for the image from the given caption. In the second stage, a diffusion model which we call unCLIP
generates the image itself from this embedding. The second model is called unCLIP because it effectively reverses the
mapping learned by the CLIP image encoder. Since it's trained to "fill in the details" necessary to produce a realistic
image from the CLIP embedding, it will learn to model all of the information that CLIP deems irrelevant for its training
objective and hence discards.

There's a few reasons why it's advantageous to use this two-stage sampling process, and we discuss two of them
here.[^why_clip] Firstly, we can explicitly allocate training compute to modeling the high-level semantics that make
images meaningful to humans. Images contain a lot of information, most of which is used to describe to fine-grained,
imperceptible details.  Only a relatively small sliver of this information is responsible for what makes images visually
coherent and meaningful to us, and the CLIP image embedding captures much of this. Training a prior model on the CLIP
image embedding allows us to focus on modeling these salient characteristics first, before filling in the details
necessary to synthesize a realistic image in the second stage.

[^why_clip]: [Our paper][paper] discusses more advantages of the two-stage sampling process.

[^house][]{-} The second reason is that CLIP's multimodal embedding space allows us to leverage
[word2vec][word2vec]-style arithmetic for image manipulation, a technique that we call _text diffs_. Let $f_i$ and $f_t$
denote the CLIP image and text encoders, respectively, and suppose that we have an image of a victorian house contained
in a file `house.png` which we would like to transform into a modern house. To do this, we first compute

$$
\begin{align}
z_{i0} &= f_i(\texttt{house.png}), \\
z_{t0} &= f_t(\textrm{"a photo of a victorian house"}), \\
z_{t1} &= f_t(\textrm{"a photo of a modern house"}), \quad\textrm{and} \\
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
[^house]: ![](posts/dalle2/images/house.gif) Animation of text diff used to
transform a victorian house into a modern one.

_Acknowledgments:_ Thanks to my coauthors [Prafulla Dhariwal][prafulla], [Alex Nichol][alex], [Casey Chu][casey], and
[Mark Chen][mark].
