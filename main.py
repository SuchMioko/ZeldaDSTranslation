import os
import io
import sys
import argparse
import binascii
import ndspy.rom
import ndspy.bmg
import subprocess
from tqdm import tqdm
from zelda import Stream
from zelda import Control


romfile = 'zelda.nds'
mainFolder = 'data/string/'
patch = 'zelda.xdelta'
tool_delta = 'xdelta3.exe'
version = '1.1'


zelda_phMessage = [
    'English/Message/battle.bmg',
    'English/Message/battleCommon.bmg',
    'English/Message/bossLast1.bmg',
    'English/Message/bossLast3.bmg',
    'English/Message/brave.bmg',
    'English/Message/collect.bmg',
    'English/Message/demo.bmg',
    'English/Message/field.bmg',
    'English/Message/flame.bmg',
    'English/Message/frost.bmg',
    'English/Message/ghost.bmg',
    'English/Message/hidari.bmg',
    'English/Message/kaitei.bmg',
    'English/Message/kaitei_F.bmg',
    'English/Message/kojima1.bmg',
    'English/Message/kojima2.bmg',
    'English/Message/kojima3.bmg',
    'English/Message/kojima5.bmg',
    'English/Message/main_isl.bmg',
    'English/Message/mainselect.bmg',
    'English/Message/myou.bmg',
    'English/Message/power.bmg',
    'English/Message/regular.bmg',
    'English/Message/sea.bmg',
    'English/Message/sennin.bmg',
    'English/Message/ship.bmg',
    'English/Message/staff.bmg',
    'English/Message/system.bmg',
    'English/Message/torii.bmg',
    'English/Message/wind.bmg',
    'English/Message/wisdom.bmg',
    'English/Message/wisdom_dngn.bmg'
]

zelda_stMessage = [
    'English/Message/battle_common.bmg',
    'English/Message/battle_parent.bmg',
    'English/Message/castle.bmg',
    'English/Message/castle_town.bmg',
    'English/Message/collect.bmg',
    'English/Message/demo.bmg',
    'English/Message/demo01_05.bmg',
    'English/Message/demo06_10.bmg',
    'English/Message/demo11_15.bmg',
    'English/Message/demo16_20.bmg',
    'English/Message/demo21_25.bmg',
    'English/Message/desert.bmg',
    'English/Message/dungeon.bmg',
    'English/Message/field.bmg',
    'English/Message/flame.bmg',
    'English/Message/flame_fld.bmg',
    'English/Message/forest.bmg',
    'English/Message/intrain.bmg',
    'English/Message/maingame.bmg',
    'English/Message/post.bmg',
    'English/Message/regular.bmg',
    'English/Message/select.bmg',
    'English/Message/shop.bmg',
    'English/Message/snow.bmg',
    'English/Message/tower.bmg',
    'English/Message/tower_lobby.bmg',
    'English/Message/train.bmg',
    'English/Message/train_extra.bmg',
    'English/Message/village.bmg',
    'English/Message/water.bmg'
]

def showProgress(iterable):
    return tqdm(iterable=iterable)

def get_args():
    parse = argparse.ArgumentParser(description='Zelda DS Translation Versi %s' % version)
    parse.add_argument(
        '-x', '--extract', action='store_true',
        help='\x1b[92mExtract text game ke file .txt\x1b[0m', default=False)
    parse.add_argument(
        '-c', '--repack', action='store_true',
        help='\x1b[92mRepack text ke dalam game\x1b[0m', default=False)
    parse.add_argument(
        '-f', '--fstring', action='store_true',
        help='\x1b[92mCari string game\x1b[0m', default=False)
    parse.add_argument(
        '-i', '--ignore', action='store_true',
        help='\x1b[92mJangan buat patch xdelta ketika repacking\x1b[0m', default=False)

    return parse


rom = ndspy.rom.NintendoDSRom.fromFile(romfile)
RomFile = []
os.makedirs(mainFolder, exist_ok=True)
subprocess.Popen('clear', shell=True).wait()
xdelta_s = tool_delta if os.path.isfile(tool_delta) else tool_delta[:7]

if str(rom.name).find('ZELDA_DS') != -1: # Header dari game Phantom Hourglass
    RomFile = zelda_phMessage
    ControlCode = Control.Phantom_Hourglass
else: # Game Spirit Track
    RomFile = zelda_stMessage
    ControlCode = Control.SpiritTrack

cli  = get_args()
args = cli.parse_args()
extract = args.extract
repack  = args.repack
fstring = args.fstring
xdelta3 = args.ignore

if extract:
    print('Extract text dari game...')
    for file in showProgress(RomFile):
        flags = True
        outFile = file.replace('.bmg', '.txt')
        files = outFile.removeprefix('English/Message/')
        with open(mainFolder + files, mode='w') as sjis:
            sjisFile = rom.getFileByName(file)
            sjisData = ndspy.bmg.BMG(sjisFile)
            f = Stream.stream(io.StringIO(''))
            for address in range(len(sjisData.messages)):
                string = sjisData.messages[address].stringParts
                f.write('[Address : {0:08d}]\n'.format(address))
                for ControlMessage in string:
                    ControlMessage = str(ControlMessage)
                    if (ControlMessage[0] == '[') and (ControlMessage[-1] == ']'):
                        ControlMessage = ControlCode[ControlMessage]
                    f.write(ControlMessage)
                f.write('\n' + '━' * 29 + '\n')
            f.seek(0, 0)
            if flags:
                sjis.write(f.read())
                flags = False
    print('File text ada di folder:\x1b[92m', mainFolder + '\x1b[0m')

if repack:
   ReverseControl = inv_map = {
       control: code for code, control in ControlCode.items()
   }
   print('Repacking ROM...')
   for file in showProgress(RomFile):
       sjissFile = rom.getFileByName(file)
       sjissData = ndspy.bmg.BMG(sjissFile)
       with open(mainFolder + file[:-3].replace('English/Message/', '') + 'txt', 'r') as sjissFile:
           sjissFile = sjissFile.read()
           sjissFile = Stream.stream(io.StringIO(sjissFile))
           for address in range(len(sjissData.messages)):
               sjissFile.readline()[-20:-2].replace('Address : ', '')
               startControl = sjissFile.string()[:-1].split('($')
               sjissplit = []
               for Control in startControl:
                   sjissplit.extend(Control.split(')'))

               sjiss = []
               for Control in sjissplit:
                   try:
                       ControlCode = ReverseControl['($' + Control + ')'][1:-1].split(':')
                       sjiss.append(ndspy.bmg.Message.Escape(
                           int(ControlCode[0]), binascii.unhexlify(ControlCode[1]))
                       )
                   except:
                       sjiss.append(Control)
                       continue
               sjissData.messages[address].stringParts = sjiss
       rom.setFileByName(file, sjissData.save())
   rom.saveToFile(romfile[:5] + '_patched.nds')
   if xdelta3 is not True:
       try:
           xdelta = subprocess.Popen(xdelta_s + ' -f -e -s \'{old_rom}\' \'{rom_baru}\' \'{patch_rom}\''.format(
               old_rom=romfile, rom_baru=romfile[:5] + '_patched.nds', patch_rom=patch,
           ), shell=True).wait()
           if xdelta != 1:
               print('\nPatch ROM berhasil dibuat dengan nama file :', patch)
       except:
           print('\x1b[91m[-] \x1b[0mGagal membuat patch ROM!')
   print('\x1b[92m[+] \x1b[0mROM baru dibuat dengan nama:', romfile[:5] + '_patched.nds')

if fstring:
   file_ = []
   text = input('string : ').encode('utf-8')
   subprocess.Popen('clear', shell=True).wait()
   for (root, dirs, files) in os.walk('data/'):
       for file in files:
            file = os.path.join(root, file)
            file_.append(file)

   for files in file_:
       with open(files, 'rb') as sjisdata:
           sjisread = sjisdata.read()
           if sjisread.find(text) != -1:
               sjisdata.seek(int(sjisread.find(text)), 0)
               print('━' * 29)
               string = sjisdata.read(100).replace(
                   b'\x00', b'\n').replace(
                       b'\xe2\x94\x81', b'\b' * 42).decode('utf-8', 'ignore'
               )
               print(
                   'Nama File =\x1b[92m', files + '\n\n\x1b[0m' + string)
