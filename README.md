# Identicon Generator (Github-like)

An [Identicon](https://en.wikipedia.org/wiki/Identicon) is an *icon* that contains a hash value representing part of your *identity*. Although it is not known how *Github* generates each user's Identicon, it's not too hard to make one.

For a 5x5 "Github-like" identicon, observe that all of them are **horizontally symmetric**, which means that the pattern itself only contains 5\*3 = 15 bits of information. Other than that, the color only contains 3 bytes of info, assuming that each of the rgb-channel takes up 8 bits. Since we don't use many bits, there is no need to compute a *strong and long* hash value. A sha1 hash would do the favor.

The tricky part is: **How to design the pattern, so that the chance of any two users having the same identicon is equally likely/unlikely?** Maybe one would come up of an idea like this: `For each hex-value in the hash string, mark the corresponding table[0:15] until the table has enough dots.` Unfortunately, this method would results in all permutations, for example 'a2ce' and 'ac2e', having the same identicon. It's likely not a good idea!

Another point one can consider is that, **since identicons are viewed by humans, two color would become indistinguishable if their pixel values are close to each other**. Consider a method in generating the dots like this: `Starting from the grid at the upper-left corner. Draw a dot if the first hex-value in the hash string is greater than 0x7, otherwise don't.` However, if two bytes from different hash strings are having values that are close to each other, not only are their color alike, the pattern are also more likely to be the same (For example, 'ad15' would have the same pattern as 'cf06' in this scenario). A better design would be: Even though the two bytes' value are close, the patterns are still decided independently.

Another point one can consider is that, **since identicons are viewed by humans, two color would become indistinguishable if their pixel values are close to each other**. Consider a method in generating the dots like this: `Starting from the grid at the upper-left corner. Draw a dot if the first hex-value in the hash string is greater than 0x7, otherwise don't.` However, if two bytes from different hash strings are having values that are close to each other, not only are their color alike, the pattern are also more likely to be the same (For example, 'ad15' would have the same pattern as 'cf06' in this scenario). A better design would be: Even though the two bytes' value are close, the patterns are still decided independently.


# Usage

* `python3 [thisProgramName.py]`
  
  <img src="/res/usage.png" alt="Screenshot" width="800"/>

* Run it online! *But no pop-up window showing the color :-(*

  https://repl.it/repls/BlaringNecessaryDecimals


# Gallery

<img src="/res/pic1.png" alt="icon1" width="200"/> <img src="/res/pic2.png" alt="icon2" width="200"/> <img src="/res/pic3.png" alt="icon3" width="200"/>

<img src="/res/pic5.png" alt="icon5" width="200"/> <img src="/res/pic6.png" alt="icon6" width="200"/> <img src="/res/pic7.png" alt="icon7" width="200"/>

<img src="/res/pic8.png" alt="icon8" width="200"/> <img src="/res/pic9.png" alt="icon9" width="200"/>

# References
1. https://github.com/donpark/identicon

    The father of identicon. He used predefined geometry patches to create the icon, which is really cool.
  
2. https://github.com/dgraham/identicon/blob/master/src/lib.rs

    He used a mod-2 method to generate the dots. My approach is pretty much similar to his.

3. https://matplotlib.org/gallery/shapes_and_collections/artist_reference.html#sphx-glr-gallery-shapes-and-collections-artist-reference-py
4. http://colorizer.org/
