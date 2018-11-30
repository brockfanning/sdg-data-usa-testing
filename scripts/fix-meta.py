# -*- coding: utf-8 -*-

import yaml
import glob
import os
import validators

def fix_meta(meta):
    if 'source_url_1' in meta:
        url = meta['source_url_1']
        if url is None:
            return meta
        elif url == '(place holder)':
            del meta['source_url_1']
            return meta
        elif validators.url(url):
            meta['source_url_text_1'] = meta['source_url_1']
        else:
            del meta['source_url_1']
            meta['source_notes_1'] = url

    return meta

def main():
    metas = glob.glob("meta/*.md")
    print("Checking " + str(len(metas)) + " metadata files...")
    for met in metas:
        with open(met, encoding="UTF-8") as stream:
            meta = next(yaml.safe_load_all(stream))
        fixed = fix_meta(meta)

        yaml_string = yaml.dump(fixed,
            default_flow_style=False,
            explicit_start=True,
            explicit_end=True)
        with open(met, "w") as output:
            output.write(yaml_string.replace("\n...\n", "\n---"))
    print("Success")

if __name__ == '__main__':
    # Set the working directory to the project root (two below)
    filepath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(filepath)
    os.chdir(os.path.join('..'))  # one level up from scripts
    main()
