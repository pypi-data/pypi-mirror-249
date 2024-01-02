#!/usr/bin/env python3
r"""This script creates a line-to-line aligned tmx file.

It accepts either two sentence-segmented files, with one sentence per line, or
one file with two tab-separated elements per line. Based on that, the script
creates a tmx file.

It accepts one tab-delimited file (format: 'original text \\t translation')
or two files: original.txt, foreign.txt, and aligns them line-to-line.

You must also pass as the first argument the desired language codes as follows:
-c en-US#ar-SA; -c EN#RU, etc.

The default language codes are en-US and ru-RU
"""

import os
import argparse
import xml.etree.ElementTree as ET


def get_data(file_paths: list):
    """Extract data from one file or two files."""
    data_count = 0
    ignored_lines_num = 0
    data = []

    if len(file_paths) > 1:
        with open(file_paths[0], 'r', encoding='utf8') as f1, \
             open(file_paths[1], 'r', encoding='utf8') as f2:
            for src, trg in zip(f1, f2):
                src, trg = src.strip(), trg.strip()
                if src and trg:
                    data_count += 1
                    data.append((src, trg))
                else:
                    ignored_lines_num += 1

    elif len(file_paths) == 1:
        with open(file_paths[0], 'r', encoding='utf8') as f1:
            for line in f1:
                line = line.strip()
                if line:
                    try:
                        src, trg = line.split('\t')
                    except ValueError as e:
                        print('Check if your data is properly formatted')
                        print('There must be 2 tab-separated elements per line')
                        print(f'Look for error in line {data_count+1}\n')
                        raise e

                    src, trg = src.strip(), trg.strip()
                    if src and trg:
                        data_count += 1
                        data.append((src, trg))
                else:
                    ignored_lines_num += 1
    print(f'Number of lines with data: {data_count}')
    print(f'Number of lines without data: {ignored_lines_num}')
    return data


def build_tree(root, src_lang_code, trg_lang_code, data):
    """Build a tree structure."""
    body = ET.SubElement(root, 'body')
    for src, trg in data:
        tu = ET.SubElement(body, 'tu')

        tuv = ET.SubElement(
            tu,
            'tuv',
            attrib={'xml:lang': src_lang_code}
            )
        seg = ET.SubElement(tuv, 'seg')
        seg.text = src

        tuv = ET.SubElement(
            tu,
            'tuv',
            attrib={'xml:lang': trg_lang_code}
            )
        seg = ET.SubElement(tuv, 'seg')
        seg.text = trg

    # wrap it in an ElementTree instance
    tree = ET.ElementTree(root)
    return tree


def indent(elem, level=0):
    """Create indentation for tree elements."""
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def build_trg_file_name(filenames):
    """Return the target file name."""
    if len(filenames) > 1:
        file1, file2 = filenames[0], filenames[1]
        head, tail1 = os.path.split(file1)
        _, tail2 = os.path.split(file2)
        target_file_name = '{}-{}.tmx'.format(os.path.splitext(tail1)[0],
                                              os.path.splitext(tail2)[0])
    elif len(filenames) == 1:
        file_name = filenames[0]
        head, tail = os.path.split(file_name)
        target_file_name = '{}.tmx'.format(os.path.splitext(tail)[0])

    return head, target_file_name


def create_tmx(language_codes, file_paths):
    """Create the tmx file."""
    if language_codes is not None:
        try:
            src_lang_code, trg_lang_code = language_codes.split('#')
            src_lang_code = src_lang_code.strip()
            trg_lang_code = trg_lang_code.strip()
        except ValueError as e:
            print('Check if the language codes are correct')
            print('There must be 2 language codes')
            print('They must be separated by the # sign')
            print('And preceeded by the -c flag')
            raise e
    else:
        src_lang_code, trg_lang_code = 'en-US', 'ru-RU'

    data = get_data(file_paths)
    root = ET.Element('tmx', attrib={'version': '1.4'})
    ET.SubElement(root, 'header', attrib={'srclang': src_lang_code})
    tree = build_tree(root, src_lang_code, trg_lang_code, data)
    indent(root)
    # Save as tmx
    head, target_file_name = build_trg_file_name(file_paths)
    dsn = os.path.join(head, target_file_name)
    tree.write(dsn, encoding='UTF-8', xml_declaration=True)
    print(f'Results written to file {dsn}')
    if len(dsn) > 256:
        print('WARNING: path length exceeds 256 characters')


def main():
    """Run the script."""
    description = """Text-to-tmx converter. Accepts one tab-delimited
    file (format: 'original text \\t translation') or two files:
    original.txt, foreign.txt, and aligns them line-to-line.
    You must also pass as the first argument the desired language
    codes as follows: -c en-US#ar-SA; -c EN#RU, etc.
    The default codes are en-US and ru-RU
    """
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        '-c',
        '--codes',
        help='Provide language codes (eg. EN-US#RU-RU)'
        )
    parser.add_argument(
        'paths',
        nargs='*',
        help='Provide one or two txt file paths'
        )
    args = parser.parse_args()

    create_tmx(args.codes, args.paths)


if __name__ == '__main__':
    main()
