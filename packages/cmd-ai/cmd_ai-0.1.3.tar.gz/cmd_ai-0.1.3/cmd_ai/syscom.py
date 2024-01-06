#!/usr/bin/env python3
"""
We create a unit, that will be the test_ unit by ln -s simoultaneously. Runs with 'pytest'
"""
import sys
import subprocess as sp
from console import fg,bg
from fire import Fire
import os
from cmd_ai import config, texts
from cmd_ai.version import __version__

# print("v... unit 'unitname' loaded, version:",__version__)


def process_syscom(cmd):

    if cmd.strip() == ".q":
        sys.exit(0)

    elif cmd.strip() == ".h":
        print(texts.HELP)

    elif cmd.strip() == ".e":

        if config.CONFIG["current_role"] == "pythonista":
            print(f"i... {fg.pink}executing script {config.CONFIG['pyscript']} ... {config.PYSCRIPT_EXISTS} {fg.default}")
            if config.PYSCRIPT_EXISTS:
                if os.path.exists(config.CONFIG['pyscript']): # and input("RUN THIS?  y/n  ")=="y":
                    sp.run(['python3', config.CONFIG['pyscript']])
                else:
                    print("... not running the (nonexisting?) script.")

        if config.CONFIG["current_role"] == "sheller" or config.CONFIG["current_role"] == "piper":
            print(f"i... executing script {config.CONFIG['shscript']} ... {config.SHSCRIPT_EXISTS}")
            if config.SHSCRIPT_EXISTS:
                if os.path.exists(config.CONFIG['shscript']): # and input("RUN THIS?  y/n  ")=="y":
                    sp.run(['bash', config.CONFIG['shscript']])
                else:
                    print("... not running the (nonexisting?) script.")

        # ANY ROLE, just source
        if config.SOURCECODE_EXISTS:
            OUTFILE = f"{config.CONFIG['sourcecode']}.{config.CONFIG['sourcecodeext']}"
            # print(OUTFILE)
            if os.path.exists(OUTFILE): # and input("RUN THIS?  y/n  ")=="y":
                #sp.run(['python3', config.CONFIG['pyscript']])
                print(" ... extension to process :  ",config.CONFIG['sourcecodeext'])
                if config.CONFIG['sourcecodeext']=="dot":
                    sp.run(['dot','-Tpng', OUTFILE, "-o", "dot.png"])
                    #dot -Tpng dd.dot -o dd.png
                else:
                    print("X... undefined extension")
            else:
                print(f"X... file {OUTFILE} not found")

    # ***************************************
    elif cmd.strip() == ".r":
        print(f"i...  {bg.green}{fg.white} RESET {bg.default}{fg.default}")
        config.messages = []#.append({"role": "system", "content": texts.role_assistant})
        config.PYSCRIPT_EXISTS = False
        config.SHSCRIPT_EXISTS = False


    elif cmd.strip().find(".l")==0 and len(cmd.strip().split(" "))==1:
        print(f'i... limit tokens = {config.CONFIG["limit_tokens"]}')
    elif cmd.strip().find(".l")==0 and len(cmd.strip().split(" "))>1:
        print(f'i... limit tokens = {config.CONFIG["limit_tokens"]}')
        if len(cmd.strip())>4 :
            tk = int(cmd.strip().split(" ")[-1])
            config.CONFIG["limit_tokens"] = tk
            print(f'i... limit tokens = {config.CONFIG["limit_tokens"]}')


    # *************************************** show models
    elif cmd.strip() == ".m":
        models = config.client.models.list()
        mids = []
        for i in models.data:
            if i.id.find("gpt") >= 0:
                mids.append(i.id)
        for i in sorted(mids):
            print("   ", i)


    # ***************************************
    elif cmd.strip() == ".p":
        print(f"i...  {bg.green}{fg.white} Python expert {bg.default}{fg.default}")
        config.messages.append({"role": "system", "content": texts.role_pythonista})
        config.CONFIG["current_role"] = "pythonista"

    # *************************************** shell expert
    elif cmd.strip() == ".s":
        print(f"i...  {bg.green}{fg.white} Shell expert {bg.default}{fg.default}")
        config.messages.append({"role": "system", "content": texts.role_sheller})
        config.CONFIG["current_role"] = "sheller"


    # *************************************** dalle
    elif cmd.strip() == ".d":
        print(f"i...  {bg.green}{fg.white} NO Dalle expert {bg.default}{fg.default}")
        config.messages.append({"role": "system", "content": texts.role_dalle})
        config.CONFIG["current_role"] = "dalle"

    # *************************************** tramslator
    elif cmd.strip() == ".t":
        print(f"i...  {bg.green}{fg.white} NO Translator from english to czech {bg.default}{fg.default}")
        config.messages.append({"role": "system", "content": texts.role_translator})
        config.CONFIG["current_role"] = "translator"

    # *************************************** assistant
    elif cmd.strip() == ".a":
        print(f"i...  {bg.green}{fg.white} Brief assistant {bg.default}{fg.default}")
        config.messages.append({"role": "system", "content": texts.role_assistant})
        config.CONFIG["current_role"] = "assistant"

    # *************************************** help
    elif cmd.strip() == ".h":
        print(texts.HELP)

    # *************************************** google functions
    elif cmd.strip() == ".g":
        if len(config.TOOLLIST)==0:
            print(f"i...  {bg.green}{fg.white} google search functions ON {bg.default}{fg.default}")
            config.TOOLLIST = [  texts.tool_searchGoogle, texts.tool_getWebContent ]
            for i in config.TOOLLIST:
                print(" ... ",i['function']['name'])
        else:
            print(f"i...  {bg.red}{fg.white} google search functions OFF NOW {bg.default}{fg.default}")
            config.TOOLLIST = []

    # *************************************** google functions
    elif cmd.strip() == ".u":
        if len(config.TOOLLIST)==0:
            print(f"i...  {bg.green}{fg.white} utility functions ON {bg.default}{fg.default}")
            config.TOOLLIST = [ texts.tool_getCzechWeather ]
            for i in config.TOOLLIST:
                print(" ... ",i['function']['name'])
        else:
            print(f"i...  {bg.red}{fg.white} utility functions OFF NOW {bg.default}{fg.default}")
            config.TOOLLIST = []


    # ***************************************
    else:
        print(f"!... {fg.red} unknown system command {fg.default}")


if __name__ == "__main__":
    print("i... in the __main__ of unitname of cmd_ai")
    Fire()
