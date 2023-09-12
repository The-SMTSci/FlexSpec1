#############################################################################
# flexspec - each science image should be matched with a comparison lamp
# image and flat image taken at the same OTA orientation to prevent errors
# due to flexure and temperature expansion indemic to the flexspec.
# However, a single comparison file and flat file may be used at user's risk.
#
# The procedure produces one response file per science/comp/flat
# 2023-05-30T12:08:51-0600 wlg
#############################################################################

procedure flexspec (scifile, compfile, flatfile, response)
   file scifile   # {prompt = '\nscifile  : '}
   file compfile  # {prompt = '\ncompfile : '}
   file flatfile  # {prompt = '\nflatfile : '}
   file response  # {prompt = '\nflatfile : '}
begin

   apall(scifile,extras=yes)     # find star trace
   print("\n")
   apall(compfile,ref=scifile,recen=no,trace=no,back=no,interactive=no) # match comp
   apall(flatfile,ref=scifile,recen=no,trace=no,back=no,interactive=no) # match comp
end
