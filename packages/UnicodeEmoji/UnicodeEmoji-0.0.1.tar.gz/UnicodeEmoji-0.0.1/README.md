# Unicode Emoji

This library provides all unicode emojis as an enum. You can use it to:

* Turn emojis into descriptions;
* Use emojis from code by textual description;
* Detecting emojis in text;

# Turn an emoji into a description
You can turn an emoji into a description (for example for sentiment analysis) by converting a string into an `Emoji` enum:

```python
from UnicodeEmoji import Emoji

print(Emoji("😸").name)

# >>> 'grinning_cat_with_smiling_eyes'

```

# Using Emojis from code by description
Sometimes it is easier to use textual descriptions of emojis in your code instead of the unicode representation directly. 

This is especially the case for emojis that are composed of multiple parts, for example the woman `technologist emoji 👩‍💻` which in some editors and terminals renders as `👩💻`. 

It can also be easier to differentiate between hard to spot differences, for example the `grinning cat 😺` and `cat face 🐱`

```python
from UnicodeEmoji import Emoji

print(f"Can you see the difference between a grinning cat {Emoji.grinning_cat} and a cat face {Emoji.cat_face}?")

# >>> Easy emojis in Python 🐍!
```

# Detecting emojis in text
It can also be useful to detect if a string contains an emoji:

```python
from UnicodeEmoji import Emoji

input = "Hi there! 😄"

all_emojis = [str(emoji) for emoji in Emoji]
input_contains_emoji = any(c in all_emojis for c in input)

print(input_contains_emoji)

# >>> True

```