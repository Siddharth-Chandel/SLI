from rich import print as pprint
from SignToVoice import Sign2Voice
from VoiceToSign import Voice2Sign
from constants import *


def run():
    while True:
        pprint(
            '''
[cyan]HELLO EVERYONE, PLEASE SELECT ONE ACTION TO PERFORM FROM BELOW :[/cyan]
1. [yellow]Sign to voice[/yellow]
2. [yellow]Voice to sign[/yellow]
3. [yellow]Exit[/yellow]
        '''
        )

        try:
            action = int(input('Your answer :- '))
            print()

            # try:
            if action == 1:
                Sign2Voice(model_path=MODEL, video_src=VIDEO)

            elif action == 2:
                Voice2Sign(img_path=IMAGE, audio_src=AUDIO)

            elif action == 3:
                break

            else:
                raise ValueError('invalid value...')

        except Exception as e:
            pprint('[red]WRONG ATTEMPT! TRY AGAIN![/red]')

    pprint("[yellow]Thanks for using ! Have a nice day...[/yellow]")


if __name__ == '__main__':
    run()
