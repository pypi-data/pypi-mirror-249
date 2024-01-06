import os
import subprocess

# Browse all files
for dir in [f for f in os.listdir() if os.path.isdir(f) and not f.startswith('_')]:
    for file in [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f != '__init__.py']:
        file_path = os.path.join(dir, file)
        print("Processing {}".format(file_path))

        with open(file_path, 'r') as f:
            text = f.read()

        delimiters = ['        >>> ', '\n        ', '"""', '\n']

        splitted_text = text.rsplit(delimiters[0], 1)
        splitted_end = splitted_text[1].split(delimiters[1], 1)

        final_text = splitted_text[0] + delimiters[0] + splitted_end[0] + delimiters[1]

        output = subprocess.run(['python', file_path], stdout=subprocess.PIPE).stdout.decode('utf-8')
        splitted_output = output.split(delimiters[3])

        remove = 0
        for line in splitted_output:
            if remove == 0:
                if line.startswith("\x1b[96m"):
                    remove = 1
                else:
                    final_text += line + delimiters[1]
            else:
                if line.endswith("\x1b[0m"):
                    remove = 0

        final_text = final_text[:-13] + '\n    ' + delimiters[2] + splitted_end[1].split(delimiters[2], 1)[1]

        with open(file_path, "w") as f:
            f.write(final_text)

        print("{} processed!\n".format(file_path))
