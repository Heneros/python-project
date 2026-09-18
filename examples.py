from pathlib import Path

contents = "I love programming.\n"
contents += "I love creating new games.\n"
contents += "I also love working with data.\n"


path = Path('pi_digits.txt')
# path.write_text(contents)

with open(path, 'a') as fileobj:
     fileobj.write(contents)