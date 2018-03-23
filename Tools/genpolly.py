#!/usr/bin/env python
"""Create AWS Polly based voices for BigWigs_Voice"""

from contextlib import closing
import os
import re
import argparse
import boto3

def getvoices(polly):
    """Use describe voices to get a list of English voices to use"""
    voices = []
    voices_avail = polly.describe_voices(LanguageCode='en-US')
    for voice in voices_avail['Voices']:
        voices.append(voice['Name'])
    return voices

def main():
    """By default build with just the Joanna voice"""
<<<<<<< HEAD
    polly = boto3.client("polly")

    voice_ids = getvoices(polly)

=======
    # Valid list of voices. Could be generated dynamically from DescribeVoices
    voice_ids = ('Joanna', 'Salli', 'Kimberly', 'Kendra', 'Ivy', 'Matthew', 'Joey', 'Justin')
>>>>>>> 2bac3354648b7b09b6a830f8c58137c3578d1923
    # Setup argument parser
    parser = argparse.ArgumentParser(description='Generate AWS Polly Voices for BigWigs_Voice')
    parser.add_argument("--voice", help="AWS Polly VoiceId", action="store",
                        choices=voice_ids, default='Joanna', dest='voice_type')
    args = parser.parse_args()

    spell_lists = ('Tools/spells-leg-raid.txt', 'Tools/spells-leg-dung.txt',
                   'Tools/spells-wod-raid.txt')
    sounds_dir = "Sounds_" + args.voice_type + "/"

    if not os.path.exists(sounds_dir):
        os.makedirs(sounds_dir)

    for spells_file in spell_lists:
        with open(spells_file, "r") as s_file:
            for spell_line in s_file:
                spell_line = spell_line.rstrip('\n')
                if not spell_line.startswith(';') and len(spell_line):
                    spell_file = sounds_dir + spell_line.split('\t')[0] + ".ogg"
                    spell_name = spell_line.split('\t')[1]
                    if "=" in spell_name:
                        spell_name = re.sub(r'(\S+)=(\S+)\b',
                                            r'<phoneme alphabet="ipa" ph="\2">\1</phoneme>',
                                            spell_name)
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
