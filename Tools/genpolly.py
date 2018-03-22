#!/usr/bin/env python
from contextlib import closing
import os
import boto3

def main():
    polly = boto3.client("polly", "us-west-2")
    spells_leg_raid = "Tools/spells-leg-raid.txt"
    spells_leg_dung = "Tools/spells-leg-dung.txt"
    spells_wod_raid = "Tools/spells-wod-raid.txt"
    # Could use Joanna, Salli, Kimberly, Kendra, Ivy, Matthew, Joey, Justin
    voice_type = "Joanna"
    sounds_dir = "Sounds_" + voice_type + "/"
    if not os.path.exists(sounds_dir):
        os.makedirs(sounds_dir)
    for spells_file in spells_leg_dung, spells_leg_raid, spells_wod_raid:
        spell_list = filter(None, open(spells_file, "r").read().splitlines())
        for spell in spell_list:
            if not spell.startswith(';'):
                spell_id = spell.split('\t')[0]
                spell_name = spell.split('\t')[1]
                spell_file = sounds_dir + spell_id + ".ogg"
                if os.path.isfile(spell_file):
                    print spell_file + " exists; skipping"
                else:
                    spell_text = spell_name + "."
                    output_file = sounds_dir + spell_id + ".ogg"
                    response = polly.synthesize_speech(Text=spell_text,
                                                       OutputFormat="ogg_vorbis",
                                                       VoiceId=voice_type)
                    if "AudioStream" in response:
                        with closing(response["AudioStream"]) as stream:
                            data = stream.read()
                            fo = open(output_file, "w+")
                            fo.write(data)
                            fo.close()

if __name__ == "__main__":
    main()

