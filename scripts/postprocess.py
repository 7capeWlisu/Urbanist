import re
import os
import glob
from fontTools import ttLib
from fontTools.varLib import instancer
from fontTools.ttLib import TTFont
from fontTools.ttLib.ttFont import newTable
from fontbakery.constants import MacStyle, FsSelection, NameID, PlatformID, WindowsEncodingID, WindowsLanguageID

def fix_italic_angle(ttFont, angle=-8.0):
  post = ttLib.getTableClass("post")()
  post.decompile(ttFont.getTableData("post"), ttFont)
  post.italicAngle = angle
  ttFont['post'] = post


def add_avar_table(ttFont):
  avar = newTable("avar")
  avar.segments = {
    "wght": {
      -1.0: -1.0,
      0: 0,
      1.0: 1.0
    },
    "ital": {
      -1.0: -1.0,
      0: 0,
      1.0: 1.0
    }
  }
  ttFont['avar'] = avar

def set_windows_subfamily_name(ttFont, subfamily_name):
  ttFont['name'].setName(
    subfamily_name, 
    NameID.FONT_SUBFAMILY_NAME,
    PlatformID.WINDOWS,
    WindowsEncodingID.UNICODE_BMP,
    WindowsLanguageID.ENGLISH_USA
  )


if __name__ == "__main__":
  # for font_path in glob.glob("../fonts/variable/Urbanist-*.ttf"):
  #   # Rename Urbanist font in variable directory
  #   new_path = re.sub(r"Urbanist-.*?\[", "Urbanist[", font_path)
  #   os.rename(font_path, new_path)
  #   print("Renaming {} to {}".format(font_path, new_path))

  # for font_path in glob.glob("../fonts/*variable/*.ttf"):
  #   # Add avar table to all variable fonts
  #   with open(font_path, "rb") as f:
  #     print("Add avar table to {}".format(font_path))
  #     ttFont = TTFont(f)
  #     add_avar_table(ttFont)
  #     ttFont.save(font_path)
  
  for font_path in glob.glob("../fonts/variable/Urbanist-Italic*.ttf"):
    # set windows subfamily name to Italic in name table
    # For Urbanist-Italic, set ttFont["head"].macStyle = MacStyle.ITALIC
    # Change OS/2.fsSelection to 0x0081 
    with open(font_path, "rb") as f:
      print("Fix italic naming in {}".format(font_path))
      ttFont = TTFont(f)
      set_windows_subfamily_name(ttFont, "Italic")
      ttFont["head"].macStyle = MacStyle.ITALIC
      ttFont['OS/2'].fsSelection = FsSelection.ITALIC
      ttFont.save(font_path)

  # for font_path in glob.glob("../fonts/ttf/*Italic.ttf"):
  #   # Fix Italic Angle
  #   with open(font_path, "rb") as f:
  #     print("Fix italic angle in {}".format(font_path))
  #     ttFont = TTFont(f)
  #     fix_italic_angle(ttFont)
  #     ttFont.save(font_path)