#!/usr/bin/env python

from contextlib import closing
import os
import re
import argparse
import boto3

def main():
    # Valid list of voices. Could be generated dynamically from DescribeVoices
    voice_ids = ('Joanna', 'Salli', 'Kimberly', 'Kendra', 'Ivy', 'Matthew', 'Joey', 'Justin')
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Generate AWS Polly Voices for BigWigs_Voice')
    parser.add_argument("--voice", help="AWS Polly VoiceId", action="store",
                        choices=voice_ids, default='Joanna', dest='voice_type')
    args = parser.parse_args()
    polly = boto3.client("polly")
    spell_lists = ('Tools/spells-leg-raid.txt', 'Tools/spells-leg-dung.txt',
                   'Tools/spells-wod-raid.txt')
    sounds_dir = "Sounds_" + args.voice_type + "/"

    if not os.path.exists(sounds_dir):
        os.makedirs(sounds_dir)

    for spells_file in spell_lists:
        for spell in filter(None, open(spells_file, "r").read().splitlines()):
            if not spell.startswith(';'):
                spell_id = spell.split('\t')[0]
                spell_name = spell.split('\t')[1]
                spell_file = sounds_dir + spell_id + ".ogg"
                if "=" in spell_name:
                    spell_name = re.sub(r'(\S+)=(\S+)\b', r'<phoneme alphabet="ipa" ph="\2">\1</phoneme>', spell_name)
                spell_name = "<speak>" + spell_name + ".</speak>"
                if not os.path.isfile(spell_file):
                    response = polly.synthesize_speech(TextType='ssml',
                                                       Text=spell_name,
                                                       OutputFormat="ogg_vorbis",
                                                       VoiceId=args.voice_type)
                    if "AudioStream" in response:
                        with closing(response["AudioStream"]) as stream:
                            data = stream.read()
                            file_out = open(spell_file, "w+")
                            file_out.write(data)
                            file_out.close()
                    else:
                        print "Warning: No AudioStream output for " + spell_name

if __name__ == "__main__":
    main()

