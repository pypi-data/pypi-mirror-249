# TrustMark - Universal Watermarking for Arbitrary Resolution Images

An Open Source, MIT licensed implementation of TrustMark watemarking for the Content Authenticity Initiative (CAI) as described in:

**TrustMark - Universal Watermarking for Arbitrary Resolution Images**

https://arxiv.org/abs/2311.18297

[Tu Bui](https://www.surrey.ac.uk/people/tu-bui) <sup>1</sup>, [Shruti Agarwal](https://research.adobe.com/person/shruti-agarwal/)  <sup>2</sup> , [John Collomosse](https://www.collomosse.com)  <sup>1,2</sup>

<sup>1</sup> DECaDE Centre for the Decentralized Digital Economy, University of Surrey, UK. \
<sup>2</sup> Adobe Research, San Jose CA.


### Quick start and example

Run `pip install trustmark to install the TrustMark package

The following example in Python shows typical usage:
```python
from trustmark import TrustMark
from PIL import Image

# initialize TrustMark 
tm=TrustMark(verbose=True, model_type='C')

# encoding example
cover = Image.open('ufo_240.jpg').convert('RGB')
tm.encode(cover, 'mysecret').save('ufo_240_C.png')

# decoding example
cover = Image.open('ufo_240_C.png').convert('RGB')
wm_secret, wm_present = tm.decode(cover)
if wm_present:
  print(f'Extracted secret: {wm_secret}')
else:
  print('No watermark detected')

# removal example
stego = Image.open('ufo_240_C.png').convert('RGB')
im_recover = tm.remove_watermark(stego)
im_recover.save('recovered.png')
```

### Repository

Refer to the [Github repo](https://github.com/adobe/trustmark) where further examples of use are also available.\

Note that models are lazy loaded upon first use


## Citation
   
If you find this work useful we request you please cite the repo and/or TrustMark paper as follows.

```
@article{trustmark,
  title={Trustmark: Universal Watermarking for Arbitrary Resolution Images},
  author={Bui, Tu and Agarwal, Shruti and Collomosse, John},
  journal = {ArXiv e-prints},
  archivePrefix = "arXiv",
  eprint = {2311.18297},
  year = 2013,
  month = nov
}    
```
